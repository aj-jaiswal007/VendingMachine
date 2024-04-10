from functools import lru_cache

from vendingmachine.common.singleton import Singleton

from .defaults import DEFAULT_CASH, CoinType
from .schemas import CoinCount


class CashRegister(metaclass=Singleton):
    coins = CoinCount(
        five=DEFAULT_CASH[CoinType.FIVE],
        ten=DEFAULT_CASH[CoinType.TEN],
        twenty=DEFAULT_CASH[CoinType.TWENTY],
        fifty=DEFAULT_CASH[CoinType.FIFTY],
        hundred=DEFAULT_CASH[CoinType.HUNDRED],
    )

    def check_if_change_possible(self, coins_deposited: CoinCount, amount_to_change: int) -> bool:
        temp_total = CoinCount(
            five=self.coins.five + coins_deposited.five,
            ten=self.coins.ten + coins_deposited.ten,
            twenty=self.coins.twenty + coins_deposited.twenty,
            fifty=self.coins.fifty + coins_deposited.fifty,
            hundred=self.coins.hundred + coins_deposited.hundred,
        )
        return temp_total.check_if_change_possible(amount_to_change)


@lru_cache
def get_register():
    return CashRegister()
