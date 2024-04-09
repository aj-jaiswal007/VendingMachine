from typing import Annotated

from fastapi import APIRouter, Depends

from vendingmachine.user import models as user_models
from vendingmachine.user.authentication import get_current_active_user
from vendingmachine.user.permission import allow_seller

from . import schemas
from .manager import ProductManager

# Only sellers can access these routes
authenticated_routes = APIRouter(
    dependencies=[Depends(get_current_active_user)],
)


@authenticated_routes.get("/products")
def get_products(product_manager: Annotated[ProductManager, Depends(ProductManager)]):
    return product_manager.list_products()


@authenticated_routes.get("/products/{product_id}")
def get_product(product_id: int, product_manager: Annotated[ProductManager, Depends(ProductManager)]):
    return product_manager.get_product(product_id)


@authenticated_routes.post("/products", dependencies=[Depends(allow_seller)])
def create_product(
    product: schemas.CreateProduct,
    current_user: Annotated[user_models.User, Depends(get_current_active_user)],
    product_manager: Annotated[ProductManager, Depends(ProductManager)],
):
    # Create a new product.
    return product_manager.create_product(product=product, created_by=current_user.id)  # type: ignore


@authenticated_routes.put("/products/{product_id}", dependencies=[Depends(allow_seller)])
def update_product(
    product_id: int,
    product: schemas.UpdateProduct,
    product_manager: Annotated[ProductManager, Depends(ProductManager)],
    current_user: Annotated[user_models.User, Depends(get_current_active_user)],
):
    return product_manager.update_product(
        current_user=current_user,
        product_id=product_id,
        product=product,
    )


@authenticated_routes.delete("/products/{product_id}", dependencies=[Depends(allow_seller)])
def delete_product(
    product_id: int,
    product_manager: Annotated[ProductManager, Depends(ProductManager)],
    current_user: Annotated[user_models.User, Depends(get_current_active_user)],
):
    return product_manager.delete_product(
        current_user=current_user,
        product_id=product_id,
    )
