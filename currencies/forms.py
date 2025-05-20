from django import forms
from currencies.models import Currency

class CurrencyConverterForm(forms.Form):
    source_currency = forms.ModelChoiceField(queryset=Currency.objects.all())
    target_currencies = forms.ModelMultipleChoiceField(
        queryset=Currency.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    amount = forms.DecimalField(min_value=0, decimal_places=2)
