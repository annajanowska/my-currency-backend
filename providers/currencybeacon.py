# providers/currencybeacon.py
import requests
from datetime import date
from decimal import Decimal
from django.conf import settings
from .base import ExchangeRateProvider

class CurrencyBeaconAdapter(ExchangeRateProvider):
    BASE_URL = "https://api.currencybeacon.com/v1"

    def get_rate(
        self,
        source_currency: str,
        exchanged_currency: str,
        at_date: date
    ) -> Decimal:
        url = f"{self.BASE_URL}/historical"
        params = {
            "base": source_currency,
            "symbols": exchanged_currency,
            "date": at_date.isoformat(),
            "api_key": settings.CURRENCYBEACON_API_KEY,
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        rate = data["rates"].get(exchanged_currency)
        if rate is None:
            raise ValueError(f"No rate for {exchanged_currency} on {at_date}")
        return Decimal(f"{rate:.6f}")
