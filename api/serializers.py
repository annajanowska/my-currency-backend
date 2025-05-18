from rest_framework import serializers
from currencies.models import Currency
from rates.models import CurrencyExchangeRate

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["id", "code", "name", "symbol"]

class ExchangeRateSerializer(serializers.ModelSerializer):
    source_currency    = serializers.CharField(source="source_currency.code")
    exchanged_currency = serializers.CharField(source="exchanged_currency.code")

    class Meta:
        model = CurrencyExchangeRate
        fields = ["source_currency", "exchanged_currency", "valuation_date", "rate_value"]
