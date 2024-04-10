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
        count_count = self.model_copy()
        total = amount
        result = CoinCount()

        values = {"five": 5, "ten": 10, "twenty": 20, "fifty": 50, "hundred": 100}

        # Calculate the change starting from the highest denomination
        # and moving down to the lowest denomination
        for denomination, count in sorted(count_count.model_dump().items(), reverse=True):
            den_value = values[denomination]
            while total >= den_value and count > 0:
                setattr(result, denomination, getattr(result, denomination) + 1)
                total -= den_value
                count -= 1

        # If total is not zero, it means we couldn't make up the change
        if total != 0:
            raise InvalidOperation("Insufficient funds to return change.")

        return result

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
