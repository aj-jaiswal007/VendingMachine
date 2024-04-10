from vendingmachine.user import models

from .. import schemas
from ..exceptions import InvalidOperation
from .base import BaseState


class HasCashState(BaseState):
    def on_deposit(self, current_user: models.User, deposit_request: schemas.DepositRequest) -> schemas.DepositResponse:
        """Deposits money into the vending machine

        Args:
            coin_type (CoinType): Choice of coin type
            quantity (int): Quantity of coins submitted

        Returns:
            schemas.DepositResponse: _description_
        """
        vm = self.vm
        if vm.in_use_by is None:
            raise InvalidOperation("Machine is not in use")

        if current_user.id != vm.in_use_by.id:
            raise InvalidOperation("Machine is in use by another user")

        # Add to deplosited coins
        vm._add_cash(deposit_request.coin_type, deposit_request.quantity)
        return schemas.DepositResponse(
            message="Coins deposited successfully.",
            coin_type=deposit_request.coin_type,
            quantity=deposit_request.quantity,
            total_deposited=vm.coins_deposited,
        )

    def on_buy(self, current_user: models.User, buy_request: schemas.BuyRequest) -> schemas.BuyResponse:
        # Buy the product
        vm = self.vm
        if vm.in_use_by.id != current_user.id:  # type: ignore
            raise InvalidOperation("Machine is in use by another user")

        return schemas.BuyResponse(message="Product bought successfully.", change=1)

    def on_reset(self, current_user: models.User) -> schemas.ResetResponse:
        from .idle import IdleState

        vm = self.vm
        coins_to_dispense = vm.coins_deposited

        # Reset the machine
        vm.coins_deposited = schemas.CoinCount()
        vm.products_selected = {}
        vm.set_state(IdleState(self.vm))

        return schemas.ResetResponse(
            message="Machine reset successfully.",
            coins_to_dispense=coins_to_dispense,
        )
