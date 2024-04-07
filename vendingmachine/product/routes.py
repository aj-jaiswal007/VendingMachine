from typing import Annotated

from fastapi import APIRouter, Depends

import vendingmachine.user.models as user_models
from vendingmachine.user.authentication import get_current_active_user

public_routes = APIRouter()
authenticated_routes = APIRouter(
    dependencies=[Depends(get_current_active_user)],
)


@authenticated_routes.get("/products/")
def get_products(current_user: Annotated[user_models.User, Depends(get_current_active_user)]):
    return {"products": []}
