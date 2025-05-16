from django.contrib import admin
from .models import CurrencyExchangeRate

@admin.register(CurrencyExchangeRate)
class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display   = ("source_currency", "exchanged_currency", "valuation_date", "rate_value")
    list_filter    = ("valuation_date", "source_currency", "exchanged_currency")
    date_hierarchy = "valuation_date"

