from django.core.management.base import BaseCommand, CommandError
from datetime import date, timedelta
from decimal import Decimal
from providers.utils import get_exchange_rate_data
from currencies.models import Currency
from rates.models import CurrencyExchangeRate

class Command(BaseCommand):
    help = (
        "Load historical exchange rates.\n"
        "Example: manage.py load_history --src EUR --tgt USD --from 2025-05-05 --to 2025-05-18"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--src", required=True, help="Source currency code (e.g. EUR)"
        )
        parser.add_argument(
            "--tgt", required=True, help="Target currency code, (e.g. USD)"
        )
        parser.add_argument(
            "--from", dest="date_from", required=True,
            help="Start date (YYYY-MM-DD)"
        )
        parser.add_argument(
            "--to", dest="date_to", required=True,
            help="End date (YYYY-MM-DD)"
        )

    def handle(self, *args, **opts):
        src_code = opts["src"].upper()
        tgt_code = opts["tgt"].upper()
        try:
            d0 = date.fromisoformat(opts["date_from"])
            d1 = date.fromisoformat(opts["date_to"])
        except ValueError as e:
            raise CommandError(f"Invalid date format: {e}")

        try:
            src = Currency.objects.get(code=src_code)
            tgt = Currency.objects.get(code=tgt_code)
        except Currency.DoesNotExist:
            raise CommandError(f"Unknown currency code: {src_code} or {tgt_code}")

        current = d0
        batch = []

        while current <= d1:
            exists = CurrencyExchangeRate.objects.filter(
                source_currency=src,
                exchanged_currency=tgt,
                valuation_date=current
            ).exists()

            if not exists:
                rate: Decimal = get_exchange_rate_data(
                    src_code, tgt_code, current, provider=None
                )
                batch.append(
                    CurrencyExchangeRate(
                        source_currency=src,
                        exchanged_currency=tgt,
                        valuation_date=current,
                        rate_value=rate
                    )
                )
                self.stdout.write(
                    f"{src_code}->{tgt_code} @ {current}: {rate}"
                )
            else:
                self.stdout.write(f"{current} (already exists)")

            current += timedelta(days=1)

            if len(batch) >= 50:
                CurrencyExchangeRate.objects.bulk_create(batch)
                batch.clear()

        if batch:
            CurrencyExchangeRate.objects.bulk_create(batch)

        self.stdout.write(self.style.SUCCESS(
            f"Historical rates for {src_code}->{tgt_code} from {d0} to {d1}"
        ))
