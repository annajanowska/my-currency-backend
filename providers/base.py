from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal

class ExchangeRateProvider(ABC):

    @abstractmethod
    def get_rate(
        self,
        source_currency: str,
        exchanged_currency: str,
        at_date: date
    ) -> Decimal:
        pass
