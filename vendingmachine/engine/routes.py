from typing import Annotated

from fastapi import APIRouter, Depends

from vendingmachine.user import models as user_models
from vendingmachine.user.authentication import get_current_active_user
from vendingmachine.user.permission import allow_buyer, allow_seller

from . import schemas
from .machine import VendingMachine, get_machine

# Only buyers can access these routes
authenticated_routes = APIRouter(
    dependencies=[Depends(get_current_active_user), Depends(allow_buyer)],
)


@authenticated_routes.post("/deposit")
def deposit(
    deposit_request: schemas.DepositRequest,
    current_user: Annotated[user_models.User, Depends(get_current_active_user)],
    vending_machine: Annotated[VendingMachine, Depends(get_machine)],
):
    return vending_machine.deposit(
        current_user=current_user,
        deposit_request=deposit_request,
    )


@authenticated_routes.post("/buy")
def buy(
    buy_request: schemas.BuyRequest,
    current_user: Annotated[user_models.User, Depends(get_current_active_user)],
    vending_machine: Annotated[VendingMachine, Depends(get_machine)],
):
    return vending_machine.buy(
        current_user=current_user,
        buy_request=buy_request,
    )


@authenticated_routes.post("/reset")
def reset(
    current_user: Annotated[user_models.User, Depends(get_current_active_user)],
    vending_machine: Annotated[VendingMachine, Depends(get_machine)],
):
    return vending_machine.reset(current_user=current_user)


@authenticated_routes.get("/check_register", dependencies=[Depends(allow_seller)])
def check_register(
    current_user: Annotated[user_models.User, Depends(get_current_active_user)],
    vending_machine: Annotated[VendingMachine, Depends(get_machine)],
):
    return vending_machine.cash_register.coins
