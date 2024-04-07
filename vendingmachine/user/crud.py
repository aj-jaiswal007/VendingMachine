from sqlalchemy.orm import Session
from . import models, schemas
from vendingmachine.common.utils import get_password_hash


def get_all_users(db: Session):
    return db.query(models.User).all()


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
