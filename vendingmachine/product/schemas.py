from typing import Optional

from pydantic import BaseModel


class BaseProduct(BaseModel):
    name: str
    description: str
    price: int
    inventory_count: int


class CreateProduct(BaseProduct):
    pass

    class Config:
        from_attributes = True


class UpdateProduct(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    inventory_count: Optional[int] = None

    class Config:
        from_attributes = True
