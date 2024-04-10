from collections import defaultdict
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
    in_use_by: Optional[models.User] = None
    coins_deposited: schemas.CoinCount = schemas.CoinCount(five=0, ten=0, twenty=0, fifty=0, hundred=0)
    # product_id: quantity
    products_selected: dict[int, int] = defaultdict(int)

    def __init__(self, product_manager: Annotated[ProductManager, Depends(ProductManager)]) -> None:
        # To avoid circular imports
        from .states.idle import IdleState

        self.product_manager = product_manager
        self.state: BaseState = IdleState(self)

    def _add_cash(self, coin_type: schemas.CoinType, quantity: int) -> None:
        self.coins_deposited.add_cash(coin_type, quantity)

    def set_state(self, state: BaseState) -> None:
        self.state = state

    def deposit(self, current_user: models.User, deposit_request: schemas.DepositRequest) -> schemas.DepositResponse:
        return self.state.on_deposit(current_user, deposit_request)

    def buy(self, current_user: models.User, buy_request: schemas.BuyRequest) -> schemas.BuyResponse:
        return self.state.on_buy(current_user, buy_request)

    def reset(self, current_user: models.User) -> schemas.ResetResponse:
        return self.state.on_reset(current_user)


def get_machine(product_manager: Annotated[ProductManager, Depends(ProductManager)]):
    return VendingMachine(product_manager=product_manager)
