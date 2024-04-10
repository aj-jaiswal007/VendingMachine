from enum import Enum


class MachineState(str, Enum):
    IDLE = "IDLE"
    HAS_CASH = "HAS_CASH"
    DISPENSING = "DISPENSING"
    CHANGE = "CHANGE"


class CoinType(str, Enum):
    FIVE = "FIVE"
    TEN = "TEN"
    TWENTY = "TWENTY"
    FIFTY = "FIFTY"
    HUNDRED = "HUNDRED"
