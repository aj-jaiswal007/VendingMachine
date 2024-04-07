from pydantic import BaseModel
from vendingmachine.user.enums import RoleName
from vendingmachine.common.database import AuditBase


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    role: RoleName = RoleName.BUYER


class UserCreate(UserBase):
    password: str


class User(UserBase, AuditBase):

    class Config:
        orm_mode = True
