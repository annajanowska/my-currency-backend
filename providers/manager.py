from datetime import date
from decimal import Decimal
from .currencybeacon import CurrencyBeaconAdapter
from .mock import MockProvider
from .base import ExchangeRateProvider

class ProviderManager:
    def __init__(self, providers=None):
        self.providers = providers or [
            CurrencyBeaconAdapter(),
            MockProvider(),
        ]

    def get_rate(
        self,
        source_currency: str,
        exchanged_currency: str,
        at_date: date = None
    ) -> Decimal:
        at_date = at_date or date.today()
        errors = []
        for provider in self.providers:
            try:
                return provider.get_rate(source_currency, exchanged_currency, at_date)
            except Exception as e:
                errors.append(f"{provider.__class__.__name__}: {e}")
        raise RuntimeError("No provider succeeded:\n" + "\n".join(errors))
