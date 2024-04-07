from sqlalchemy.orm import Session

from . import models, schemas
from .authentication import get_password_hash


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        hashed_password=get_password_hash(user.password),
    )  # type: ignore
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def is_user_exists(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first() is not None


def update_user(db: Session, current_user: models.User, user_data: schemas.UserUpdate):
    for key, value in user_data.model_dump().items():
        if value:
            setattr(current_user, key, value)

    db.commit()
    db.refresh(current_user)
    return current_user
