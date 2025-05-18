from django.db import models
from currencies.models import Currency

class CurrencyExchangeRate(models.Model):
    source_currency    = models.ForeignKey(Currency, related_name="exchanges", on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date     = models.DateField(db_index=True)
    rate_value         = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)

    class Meta:
        unique_together = (("source_currency","exchanged_currency","valuation_date"),)
        ordering        = ("-valuation_date",)

    def __str__(self):
        return f"{self.source_currency.code}->{self.exchanged_currency.code} @ {self.valuation_date}"
