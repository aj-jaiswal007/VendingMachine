from vendingmachine.common.logger import logger
from vendingmachine.user import models as user_models

from .. import schemas
from ..exceptions import InvalidOperation
from .base import BaseState
from .buying import BuyingState


class IdleState(BaseState):
    def __init__(self, vm) -> None:
        super().__init__(vm)
        # Reset the machine state
        self.vm.in_use_by = None
        self.vm.coins_deposited = schemas.CoinCount()
        self.vm.coins_to_dispense = schemas.CoinCount()

    def on_deposit(self, current_user: user_models.User, deposit_request: schemas.DepositRequest):
        """Deposits money into the vending machine

        Args:
            coin_type (CoinType): Choice of coin type
            quantity (int): Quantity of coins submitted

        Returns:
            schemas.DepositResponse: _description_
        """
        logger.info(f"Depositing money. {deposit_request}")
        self.vm.coins_deposited.add_coin(deposit_request.coin_type, deposit_request.quantity)
        self.vm.in_use_by = current_user
        self.vm.set_state(BuyingState(self.vm))

    def on_buy(self, current_user: user_models.User, buy_request: schemas.BuyRequest):
        raise InvalidOperation("Please deposit coins first.")

    def on_reset(self, current_user: user_models.User):
        raise InvalidOperation("Machine is already idle.")

    def on_dispense_coin(self, current_user: user_models.User) -> schemas.CoinCount:
        raise InvalidOperation("Cannot dispense coins in idle state.")

    def on_dispense_product(self, current_user: user_models.User, product_id: int, quantity: int):
        raise InvalidOperation("Please deposit coins first.")
