import random
from datetime import date
from decimal import Decimal
from .base import ExchangeRateProvider

class MockProvider(ExchangeRateProvider):
    def get_rate(
        self,
        source_currency: str,
        exchanged_currency: str,
        at_date: date
    ) -> Decimal:
        seed = hash((source_currency, exchanged_currency, at_date))
        random.seed(seed)
        rate = 0.5 + random.random()
        return Decimal(f"{rate:.6f}")
