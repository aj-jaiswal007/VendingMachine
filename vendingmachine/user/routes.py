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

router = APIRouter()


@router.post("/token")
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
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.get("/users/me")
def get_user(current_user: Annotated[models.User, Depends(get_current_active_user)]):
    return schemas.User.model_validate(current_user)


@router.post("/users/")
def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
    if crud.is_user_exists(db, user.username):
        msg = "User already exists! Use a different username."
        logger.warning(msg)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

    return schemas.User.model_validate(crud.create_user(db, user))
