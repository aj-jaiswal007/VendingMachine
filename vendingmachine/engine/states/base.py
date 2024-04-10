from abc import ABC, abstractmethod

from vendingmachine.engine import schemas
from vendingmachine.user import models as user_models

from ..exceptions import InvalidOperation


class BaseState(ABC):
    def __init__(self, vm) -> None:
        from vendingmachine.engine.machine import VendingMachine

        self.vm: "VendingMachine" = vm

    def _validate_current_user(self, current_user: user_models.User) -> None:
        if self.vm.in_use_by is None:
            raise InvalidOperation("Machine is not in use")

        if current_user.id != self.vm.in_use_by.id:
            raise InvalidOperation("Machine is in use by another user")

    @abstractmethod
    def on_deposit(
        self,
        current_user: user_models.User,
        deposit_request: schemas.DepositRequest,
    ):
        ...

    @abstractmethod
    def on_buy(
        self,
        current_user: user_models.User,
        buy_request: schemas.BuyRequest,
    ) -> int:
        ...

    @abstractmethod
    def on_reset(
        self,
        current_user: user_models.User,
    ):
        ...

    @abstractmethod
    def on_dispense_coin(
        self,
        current_user: user_models.User,
    ) -> schemas.CoinCount:
        ...

    @abstractmethod
    def on_dispense_product(self, current_user: user_models.User, product_id: int, quantity: int):
        ...
