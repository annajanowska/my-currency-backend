from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from currencies.models import Currency
from rates.models import CurrencyExchangeRate
from providers.utils import get_exchange_rate_data
from .serializers import CurrencySerializer, ExchangeRateSerializer

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class RateListView(APIView):
    """
    GET /api/rates/?source_currency=cur&date_from=YYYY-MM-DD&date_to=YYYY-MM-DD
    """
    def get(self, request):
        src = request.query_params.get("source_currency")
        df  = request.query_params.get("date_from")
        dt  = request.query_params.get("date_to")
        if not (src and df and dt):
            return Response({"detail":"source_currency, date_from and date_to are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            date_from = datetime.fromisoformat(df).date()
            date_to   = datetime.fromisoformat(dt).date()
        except ValueError:
            return Response({"detail":"Dates must be YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            src_obj = Currency.objects.get(code=src)
        except Currency.DoesNotExist:
            return Response({"detail":f"Unknown source currency {src}"}, status=status.HTTP_404_NOT_FOUND)

        result = []
        current = date_from
        while current <= date_to:
            rates_qs = CurrencyExchangeRate.objects.filter(
                source_currency=src_obj,
                valuation_date=current
            )
            existing = {r.exchanged_currency.code: r for r in rates_qs}
            day = {"date": current.isoformat(), "rates": {}}

            for tgt_obj in Currency.objects.exclude(code=src):
                code = tgt_obj.code
                if code in existing:
                    val = existing[code].rate_value
                else:
                    val = get_exchange_rate_data(src, code, current, provider=None)
                    CurrencyExchangeRate.objects.create(
                        source_currency=src_obj,
                        exchanged_currency=tgt_obj,
                        valuation_date=current,
                        rate_value=val
                    )
                day["rates"][code] = val
            result.append(day)
            current = current.fromordinal(current.toordinal() + 1)

        return Response(result)

class ConvertView(APIView):
    """
    GET /api/convert/?source_currency=cur&exchanged_currency=cur&amount=a
    """
    def get(self, request):
        src = request.query_params.get("source_currency")
        tgt = request.query_params.get("exchanged_currency")
        amt = request.query_params.get("amount")
        if not (src and tgt and amt):
            return Response({"detail":"source_currency, exchanged_currency and amount are required"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            amount = float(amt)
        except ValueError:
            return Response({"detail":"amount must be a number"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rate = get_exchange_rate_data(src, tgt, datetime.today().date(), provider=None)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        converted = amount * float(rate)
        return Response({
            "source_currency": src,
            "exchanged_currency": tgt,
            "rate": rate,
            "amount": amount,
            "converted_amount": converted,
        })
