from vendingmachine.common.singleton import Singleton


class RateLimiter(metaclass=Singleton):
    RATE_LIMIT_PER_API_PERMIN = 20

    __cache = {}
    """
    {
        "/deposit": {
            "updated_at" "datetime",
            "count" : 0
        }
    }
    """

    def __init__(self):
        self._rate_limit = 0
