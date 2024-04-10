from typing import Optional

from pydantic import BaseModel

from vendingmachine.common.database import AuditBase
from vendingmachine.user.enums import RoleName


class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]


class User(UserBase, AuditBase):
    role: RoleName

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    roles: list[RoleName]


class Credentials(BaseModel):
    username: str
    password: str
