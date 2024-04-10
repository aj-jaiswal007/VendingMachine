from functools import lru_cache

from vendingmachine.common.singleton import Singleton

from .schemas import CoinCount


class CashRegister(metaclass=Singleton):
    coins = CoinCount(five=0, ten=0, twenty=0, fifty=0, hundred=0)


@lru_cache
def get_register():
    return CashRegister()
