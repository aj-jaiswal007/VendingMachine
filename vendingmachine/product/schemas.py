from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseProduct(BaseModel):
    name: str
    description: str
    price: int
    inventory_count: int


class CreateProduct(BaseProduct):
    model_config = ConfigDict(from_attributes=True)


class UpdateProduct(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    inventory_count: Optional[int] = None

    # Class Config
    model_config = ConfigDict(from_attributes=True)
