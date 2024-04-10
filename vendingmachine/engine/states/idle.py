from vendingmachine.common.logger import logger
from vendingmachine.user import models

from .. import schemas
from ..exceptions import InvalidOperation
from .base import BaseState
from .has_cash import HasCashState


class IdleState(BaseState):
    def on_deposit(self, current_user: models.User, deposit_request: schemas.DepositRequest) -> schemas.DepositResponse:
        """Deposits money into the vending machine

        Args:
            coin_type (CoinType): Choice of coin type
            quantity (int): Quantity of coins submitted

        Returns:
            schemas.DepositResponse: _description_
        """

        vm = self.vm
        logger.info("Entering HasCashState from IdleState.")
        vm._add_cash(deposit_request.coin_type, deposit_request.quantity)
        vm.set_state(HasCashState(vm))
        vm.in_use_by = current_user
        return schemas.DepositResponse(
            message="Coins deposited successfully.",
            coin_type=deposit_request.coin_type,
            quantity=deposit_request.quantity,
            total_deposited=vm.coins_deposited,
        )

    def on_buy(self, current_user: models.User, buy_request: schemas.BuyRequest) -> schemas.BuyResponse:
        raise InvalidOperation("Please deposit coins first.")

    def on_reset(self, current_user: models.User) -> schemas.ResetResponse:
        raise InvalidOperation("Machine is already idle.")
