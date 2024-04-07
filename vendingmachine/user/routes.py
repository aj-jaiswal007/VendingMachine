from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from vendingmachine.common.database import get_db
from vendingmachine.common.logger import logger
from vendingmachine.settings import Settings, get_settings

from . import crud, models, schemas
from .authentication import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
)
from .enums import RoleName

public_routes = APIRouter()
authenticated_routes = APIRouter(
    dependencies=[Depends(get_current_active_user)],
)


@public_routes.post("/token")
def login_for_access_token(
    credentials: schemas.Credentials,
    db: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> schemas.Token:
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={
            "id": user.id,
            "sub": user.username,
            "roles": (
                [user.role] if user.role == RoleName.BUYER else [RoleName.BUYER, RoleName.SELLER]  # type: ignore
            ),
        },
        expires_delta=access_token_expires,
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@public_routes.post("/users/")
def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):

    existing_user = crud.get_user(db, user.username)
    if existing_user is not None:
        if existing_user.is_active:  # type: ignore
            msg = "User already exists! Use a different username."
            logger.warning(msg)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

        existing_user.is_active = True  # type: ignore
        db.commit()
        return schemas.User.model_validate(existing_user)

    return schemas.User.model_validate(crud.create_user(db, user))


@authenticated_routes.get("/users/me")
def get_user(current_user: Annotated[models.User, Depends(get_current_active_user)]):
    return schemas.User.model_validate(current_user)


@authenticated_routes.put("/users/me")
def update_user(
    user_data: schemas.UserUpdate,
    current_user: Annotated[models.User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
):
    return schemas.User.model_validate(crud.update_user(db, current_user, user_data))


@authenticated_routes.delete("/users/me")
def delete_user(
    current_user: Annotated[models.User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
):
    current_user.is_active = False  # type: ignore
    db.commit()
    return {"message": "User deleted successfully."}
