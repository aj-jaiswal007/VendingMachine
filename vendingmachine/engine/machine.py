from typing import Annotated, Optional

from fastapi import Depends

from vendingmachine.common.singleton import Singleton
from vendingmachine.product.manager import ProductManager
from vendingmachine.user import models

from . import schemas
from .cash_register import CashRegister, get_register
from .states.base import BaseState


class VendingMachine(metaclass=Singleton):
    cash_register: CashRegister = get_register()

    # To be resetted after each transaction is done
    # This will be updated over the lifecycle of machine
    in_use_by: Optional[models.User] = None
    coins_deposited: schemas.CoinCount = schemas.CoinCount()
    coins_to_dispense: schemas.CoinCount = schemas.CoinCount()

    def __init__(self, product_manager: Annotated[ProductManager, Depends(ProductManager)]) -> None:
        # To avoid circular imports
        from .states.idle import IdleState

        self.product_manager = product_manager
        self.state: BaseState = IdleState(self)

    def set_state(self, state: BaseState) -> None:
        self.state = state

    def deposit(self, current_user: models.User, deposit_request: schemas.DepositRequest) -> schemas.DepositResponse:
        # Depositing coins in current state
        self.state.on_deposit(current_user, deposit_request)

        # returning response
        return schemas.DepositResponse(
            message="Coins deposited successfully.",
            coin_type=deposit_request.coin_type,
            quantity=deposit_request.quantity,
            total_deposited=self.coins_deposited,
        )

    def buy(self, current_user: models.User, buy_request: schemas.BuyRequest) -> schemas.BuyResponse:
        # This will be updated over the lifecycle of machine
        deposited = self.coins_deposited
        # Do the buying stuff
        money_spent = self.state.on_buy(current_user, buy_request)
        self.state.on_dispense_product(current_user, buy_request.product_id, buy_request.quantity)
        coins_dispensed = self.state.on_dispense_coin(current_user)
        # Returning
        return schemas.BuyResponse(
            message="Product bought successfully.",
            deposited=deposited,
            spent=money_spent,
            change=coins_dispensed,
            products=buy_request,
        )

    def reset(self, current_user: models.User) -> schemas.ResetResponse:
        # dispense coins if any
        coins_to_dispense = self.state.on_dispense_coin(current_user)

        # Returning
        return schemas.ResetResponse(
            message="Machine reset successfully.",
            change=coins_to_dispense,
        )


def get_machine(product_manager: Annotated[ProductManager, Depends(ProductManager)]):
    return VendingMachine(product_manager=product_manager)
