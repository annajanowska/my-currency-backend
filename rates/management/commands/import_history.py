import json
from django.core.management.base import BaseCommand, CommandError
from currencies.models import Currency
from rates.models import CurrencyExchangeRate
from decimal import Decimal
from datetime import date

class Command(BaseCommand):
    help = "Import historical exchange rates data  (JSON file)"

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Path to JSON file')

    def handle(self, *args, **options):
        filepath = options['filepath']
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except Exception as e:
            raise CommandError(f"Error loading JSON file: {e}")

        count = 0
        for item in data:
            try:
                src = Currency.objects.get(code=item['source_currency'])
                tgt = Currency.objects.get(code=item['exchanged_currency'])
                valuation_date = date.fromisoformat(item['valuation_date'])
                rate_value = Decimal(item['rate_value'])
            except Exception as e:
                self.stderr.write(f"Skipping invalid record: {item} ({e})")
                continue

            obj, created = CurrencyExchangeRate.objects.update_or_create(
                source_currency=src,
                exchanged_currency=tgt,
                valuation_date=valuation_date,
                defaults={'rate_value': rate_value}
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Imported {count} records from {filepath}"))
