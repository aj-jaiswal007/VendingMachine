from typing import Optional

from pydantic import BaseModel

from .enums import CoinType
from .exceptions import InvalidOperation


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

    def add(self, coin_type: CoinType, quantity: int):
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

    def add_coins(self, coins: "CoinCount"):
        self.five += coins.five
        self.ten += coins.ten
        self.twenty += coins.twenty
        self.fifty += coins.fifty
        self.hundred += coins.hundred

    def remove_coins(self, coins: "CoinCount"):
        self.five -= coins.five
        self.ten -= coins.ten
        self.twenty -= coins.twenty
        self.fifty -= coins.fifty
        self.hundred -= coins.hundred

    def get_denomination_for_amount(self, amount: int) -> "CoinCount":
        hundred_count = self.hundred
        fifty_count = self.fifty
        twenty_count = self.twenty
        ten_count = self.ten
        five_count = self.five

        denomination = CoinCount()
        # Greedy algorithm to get the denomination
        # Raise InsufficientFunds if not possible
        while amount > 0:
            if amount >= 100 and hundred_count > 0:
                amount -= 100
                hundred_count -= 1
                denomination.hundred += 1
            elif amount >= 50 and fifty_count > 0:
                amount -= 50
                fifty_count -= 1
                denomination.fifty += 1
            elif amount >= 20 and twenty_count > 0:
                amount -= 20
                twenty_count -= 1
                denomination.twenty += 1
            elif amount >= 10 and ten_count > 0:
                amount -= 10
                ten_count -= 1
                denomination.ten += 1
            elif amount >= 5 and five_count > 0:
                amount -= 5
                five_count -= 1
                denomination.five += 1
            else:
                raise InvalidOperation("Insufficient funds to return change.")

        return denomination

    def check_if_change_possible(self, amount: int) -> bool:
        if self.total < amount:
            return False

        try:
            self.get_denomination_for_amount(amount)
        except InvalidOperation:
            return False

        return True


class DepositResponse(DepositRequest):
    message: str
    total_deposited: CoinCount


class ResetResponse(BaseModel):
    message: str
    change: Optional[CoinCount] = None


class BuyResponse(BaseModel):
    message: str
    deposited: CoinCount
    spent: int
    change: Optional[CoinCount]
    products: BuyRequest
