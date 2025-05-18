from datetime import date
from decimal import Decimal
from .base import ExchangeRateProvider
from django.apps import apps
from django.utils.module_loading import import_string

class ProviderManager:
    def __init__(self):
        ProviderModel = apps.get_model("providers", "Provider")
        qs = ProviderModel.objects.filter(is_active=True).order_by("priority")

        self.providers: list[ExchangeRateProvider] = []
        for cfg in qs:
            try:
                AdapterClass = import_string(cfg.class_path)
                adapter = AdapterClass()
                self.providers.append(adapter)
            except Exception as e:
                print(f"[ProviderManager] Failed to load {cfg.name}: {e}")

        if not self.providers:
            from .currencybeacon import CurrencyBeaconAdapter
            from .mock import MockProvider
            self.providers = [CurrencyBeaconAdapter(), MockProvider()]

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
