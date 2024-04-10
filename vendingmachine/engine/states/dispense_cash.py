from vendingmachine.common.logger import logger
from vendingmachine.engine.exceptions import InvalidOperation
from vendingmachine.engine.schemas import BuyRequest, CoinCount
from vendingmachine.user.models import User

from .base import BaseState


class DispenseCashState(BaseState):
    def on_buy(self, current_user: User, buy_request: BuyRequest):
        raise InvalidOperation("I am dispensing money now, please don't interfere.")

    def on_deposit(self, current_user: User, deposit_request: BuyRequest):
        raise InvalidOperation("I am dispensing money now, You cannot add any money.")

    def on_reset(self, current_user: User):
        raise InvalidOperation("I am dispensing money now, You cannot reset me.")

    def on_dispense_product(self, current_user: User, product_id: int, quantity: int):
        raise InvalidOperation("I am dispensing cash now, You cannot buy anything.")

    def on_dispense_coin(self, current_user: User) -> CoinCount:
        self._validate_current_user(current_user)
        amount_to_dispense = self.vm.coins_to_dispense
        logger.info("Dispensing cash now....")
        logger.info(f"Dispensing cash: {amount_to_dispense}")
        # Go to idle state
        from .idle import IdleState

        self.vm.set_state(IdleState(self.vm))
        return amount_to_dispense
