from fastapi import APIRouter, Depends
from vendingmachine.common.logger import logger
from vendingmachine.common.database import get_db
from sqlalchemy.orm import Session
from . import crud
from . import schemas

router = APIRouter()


@router.get("/users/")
def get_all_users(db: Session = Depends(get_db)):
    logger.info("Get all users API called!")
    return crud.get_all_users(db)


@router.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info("Create user API called!")
    return crud.create_user(db, user)
