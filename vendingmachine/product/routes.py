from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from vendingmachine.common.database import get_db
from vendingmachine.user import models as user_models
from vendingmachine.user.authentication import get_current_active_user
from vendingmachine.user.permission import allow_seller

from . import models, schemas

# Only sellers can access these routes
authenticated_routes = APIRouter(
    dependencies=[Depends(get_current_active_user)],
)


@authenticated_routes.get("/products/")
def get_products(db: Annotated[Session, Depends(get_db)]):
    return db.query(models.Product).all()


@authenticated_routes.post("/products/", dependencies=[Depends(allow_seller)])
def create_product(
    product: schemas.CreateProduct,
    current_user: Annotated[user_models.User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
):
    # Create a new product.
    ...
    return []
