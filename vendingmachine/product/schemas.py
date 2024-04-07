from pydantic import BaseModel


class BaseProduct(BaseModel):
    name: str
    description: str
    price: int


class CreateProduct(BaseProduct):
    pass

    class Config:
        orm_mode = True
