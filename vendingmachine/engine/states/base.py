from abc import ABC, abstractmethod

from vendingmachine.user import models

from .. import schemas


class BaseState(ABC):
    def __init__(self, vm) -> None:
        from vendingmachine.engine.machine import VendingMachine

        self.vm: "VendingMachine" = vm

    @abstractmethod
    def on_deposit(
        self,
        current_user: models.User,
        deposit_request: schemas.DepositRequest,
    ) -> schemas.DepositResponse:
        ...

    @abstractmethod
    def on_buy(
        self,
        current_user: models.User,
        buy_request: schemas.BuyRequest,
    ) -> schemas.BuyResponse:
        ...

    @abstractmethod
    def on_reset(
        self,
        current_user: models.User,
    ) -> schemas.ResetResponse:
        ...
