import asyncio
import aiohttp
from datetime import date, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from currencies.models import Currency
from rates.models import CurrencyExchangeRate
from django.conf import settings

BASE_URL = "https://api.currencybeacon.com/v1/historical"
API_KEY = settings.CURRENCYBEACON_API_KEY

class Command(BaseCommand):
    help = "Asynchronously load historical exchange rates"

    def add_arguments(self, parser):
        parser.add_argument("--src", required=True, help="Source currency code (e.g. EUR)")
        parser.add_argument("--tgt", required=True, help="Target currency code (e.g. USD)")
        parser.add_argument("--from", dest="date_from", required=True, help="Start date (YYYY-MM-DD)")
        parser.add_argument("--to", dest="date_to", required=True, help="End date (YYYY-MM-DD)")

    async def fetch_rate(self, session, src_code, tgt_code, dt):
        params = {
            "base": src_code,
            "symbols": tgt_code,
            "date": dt.isoformat(),
            "api_key": API_KEY
        }
        try:
            async with session.get(BASE_URL, params=params, timeout=10) as response:
                data = await response.json()
                rate = data["rates"].get(tgt_code)
                if rate is None:
                    raise ValueError(f"No rate for {tgt_code} on {dt}")
                return (dt, Decimal(str(rate)))
        except Exception as e:
            print(f"Error fetching {src_code}->{tgt_code} @ {dt}: {e}")
            return None

    async def gather_rates(self, src_code, tgt_code, start_date, end_date):
        results = []
        async with aiohttp.ClientSession() as session:
            tasks = []
            current = start_date
            while current <= end_date:
                tasks.append(self.fetch_rate(session, src_code, tgt_code, current))
                current += timedelta(days=1)
            all_results = await asyncio.gather(*tasks)
            results = [res for res in all_results if res]
            return results

    def handle(self, *args, **options):
        try:
            src_code = options["src"].upper()
            tgt_code = options["tgt"].upper()
            d0 = date.fromisoformat(options["date_from"])
            d1 = date.fromisoformat(options["date_to"])
        except Exception as e:
            raise CommandError(f"Invalid input: {e}")

        try:
            src_obj = Currency.objects.get(code=src_code)
            tgt_obj = Currency.objects.get(code=tgt_code)
        except Currency.DoesNotExist:
            raise CommandError("Currency code not found in database")

        self.stdout.write(f"Loading {src_code}->{tgt_code} from {d0} to {d1}...")

        results = asyncio.run(self.gather_rates(src_code, tgt_code, d0, d1))

        records = [
            CurrencyExchangeRate(
                source_currency=src_obj,
                exchanged_currency=tgt_obj,
                valuation_date=valuation_date,
                rate_value=rate_value
            )
            for valuation_date, rate_value in results
        ]

        CurrencyExchangeRate.objects.bulk_create(records, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f"Imported {len(records)} rates."))

