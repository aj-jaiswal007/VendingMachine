from vendingmachine.common.logger import logger
from vendingmachine.engine.exceptions import InvalidOperation
from vendingmachine.engine.schemas import BuyRequest, CoinCount, DepositRequest
from vendingmachine.user.models import User

from .base import BaseState


class DispenseProductState(BaseState):
    def on_buy(self, current_user: User, buy_request: BuyRequest) -> int:
        raise InvalidOperation("Dispensing products now. Please wait for the product to be dispensed.")

    def on_deposit(self, current_user: User, deposit_request: DepositRequest):
        raise InvalidOperation("Dispensing products now. Please wait for the product to be dispensed.")

    def on_reset(self, current_user: User):
        raise InvalidOperation("Dispensing products now. Machine will auto reset after done.")

    def on_dispense_product(self, current_user: User, product_id: int, quantity: int):
        self._validate_current_user(current_user)
        # Just need to dispense the product now

        logger.info(f"Dispensing product now....: product={product_id}, qty={quantity}")
        # Reducing product inventory
        self.vm.product_manager.reduce_product_inventory(product_id=product_id, quantity=quantity)
        product = self.vm.product_manager.get_product(product_id=product_id)
        amount_to_charge: int = product.price * quantity  # type: ignore
        amount_to_refund = self.vm.coins_deposited.total - amount_to_charge

        # Adding amount to the cash register
        self.vm.cash_register.coins.add_coins(self.vm.coins_deposited)
        # Resetting deposited coins
        self.vm.coins_deposited = CoinCount()
        # Setting coints to dispense fo dispense coin state can handle.
        self.vm.coins_to_dispense = self.vm.cash_register.coins.get_denomination_for_amount(amount_to_refund)

        from .dispense_cash import DispenseCashState

        self.vm.set_state(DispenseCashState(self.vm))

    def on_dispense_coin(self, current_user: User):
        raise InvalidOperation("Dispensing products now. Change will be auto dispensed.")
