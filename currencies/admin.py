from django.contrib import admin
from .models import Currency
from django.urls import path
from django.shortcuts import render
from .forms import CurrencyConverterForm
from providers.utils import get_exchange_rate_data
from datetime import date

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display  = ("code", "name", "symbol")
    search_fields = ("code", "name")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('converter/', self.admin_site.admin_view(self.currency_converter_view), name='currency_converter'),
        ]
        return custom_urls + urls

    def currency_converter_view(self, request):
        result = None
        if request.method == 'POST':
            form = CurrencyConverterForm(request.POST)
            if form.is_valid():
                source = form.cleaned_data['source_currency']
                targets = form.cleaned_data['target_currencies']
                amount = form.cleaned_data['amount']
                result = {}
                for tgt in targets:
                    rate = get_exchange_rate_data(source.code, tgt.code, date.today())
                    result[tgt.code] = amount * rate
        else:
            form = CurrencyConverterForm()
        context = {
            'form': form,
            'result': result,
            'title': 'Currency Converter',
        }
        return render(request, 'admin/currency_converter.html', context)
