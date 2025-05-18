from datetime import date
from decimal import Decimal
from .base import ExchangeRateProvider
from .manager import ProviderManager

def get_exchange_rate_data(
    source_currency: str,
    exchanged_currency: str,
    valuation_date: date,
    provider: ExchangeRateProvider = None
) -> Decimal:

    if provider:
        return provider.get_rate(source_currency, exchanged_currency, valuation_date)
    return ProviderManager().get_rate(source_currency, exchanged_currency, valuation_date)
