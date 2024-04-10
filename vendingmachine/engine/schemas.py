from pydantic import BaseModel

from .enums import CoinType
from .exceptions import InvalidOperation


class BuyResponse(BaseModel):
    message: str
    change: int


class ChangeResponse(BaseModel):
    message: str
    change: int


class DepositRequest(BaseModel):
    coin_type: CoinType
    quantity: int


class BuyRequest(BaseModel):
    product_id: int
    quantity: int


class CoinCount(BaseModel):
    five: int = 0
    ten: int = 0
    twenty: int = 0
    fifty: int = 0
    hundred: int = 0

    @property
    def total(self):
        return self.five * 5 + self.ten * 10 + self.twenty * 20 + self.fifty * 50 + self.hundred * 100

    def add_cash(self, coin_type: CoinType, quantity: int):
        if coin_type == CoinType.FIVE:
            self.five += quantity
        elif coin_type == CoinType.TEN:
            self.ten += quantity
        elif coin_type == CoinType.TWENTY:
            self.twenty += quantity
        elif coin_type == CoinType.FIFTY:
            self.fifty += quantity
        elif coin_type == CoinType.HUNDRED:
            self.hundred += quantity
        else:
            raise InvalidOperation("Invalid coin type")


class DepositResponse(DepositRequest):
    message: str
    total_deposited: CoinCount


class ResetResponse(BaseModel):
    message: str
    coins_to_dispense: CoinCount
