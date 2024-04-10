from vendingmachine.common.logger import logger
from vendingmachine.user import models as user_models

from .. import schemas
from ..exceptions import InvalidOperation
from .base import BaseState


class BuyingState(BaseState):
    def on_deposit(self, current_user: user_models.User, deposit_request: schemas.DepositRequest):
        """Deposits money into the vending machine

        Args:
            coin_type (CoinType): Choice of coin type
            quantity (int): Quantity of coins submitted

        Returns:
            schemas.DepositResponse: _description_
        """
        self._validate_current_user(current_user)
        logger.info(f"Depositing money. {deposit_request}")
        self.vm.coins_deposited.add(deposit_request.coin_type, deposit_request.quantity)

    def on_buy(self, current_user: user_models.User, buy_request: schemas.BuyRequest) -> int:
        # Buy the product
        self._validate_current_user(current_user)

        product = self.vm.product_manager.get_product(product_id=buy_request.product_id)
        if product is None:
            raise InvalidOperation("Product not found")

        # Check if the product is available
        product_inventory = self.vm.product_manager.get_product_inventory(product_id=buy_request.product_id)
        if product_inventory.quantity < buy_request.quantity:  # type: ignore
            raise InvalidOperation(
                f"We have only {product_inventory.quantity} units of {product.name} left. Order less quantity."
            )

        # Check the total price is less than or equal to the total deposited
        total_price: int = product.price * buy_request.quantity  # type: ignore
        total_deposited = self.vm.coins_deposited.total
        if total_price > total_deposited:
            raise InvalidOperation("Insufficient funds add more money or reset to collect your money.")

        # Check if change is possible to return
        amount_to_change: int = total_deposited - total_price  # type: ignore
        is_change_possible = self.vm.cash_register.check_if_change_possible(
            coins_deposited=self.vm.coins_deposited,
            amount_to_change=amount_to_change,
        )
        if not is_change_possible:
            raise InvalidOperation("Cannot return change. Please add exact amount or reset to collect your money.")

        # All is good we may move to product dispensing state now
        from .dispense_product import DispenseProductState

        self.vm.set_state(DispenseProductState(self.vm))

        # amount spent
        return total_price

    def on_reset(self, current_user: user_models.User):
        # Flush the coins collected
        self._validate_current_user(current_user)
        self.vm.coins_to_dispense = self.vm.coins_deposited
        self.vm.coins_deposited = schemas.CoinCount()
        from .dispense_cash import DispenseCashState

        self.vm.set_state(DispenseCashState(self.vm))

    def on_dispense_coin(self, current_user: user_models.User):
        raise InvalidOperation("Cannot dispense coins in this state.")

    def on_dispense_product(self, current_user: user_models.User, product_id: int, quantity: int):
        raise InvalidOperation("Cannot dispense product in this state.")
