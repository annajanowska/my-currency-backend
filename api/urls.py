from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrencyViewSet, RateListView, ConvertView

app_name = "v1"

router = DefaultRouter()
router.register(r"currencies", CurrencyViewSet, basename="currency")

urlpatterns = [
    path("", include(router.urls)),
    path("rates/", RateListView.as_view(), name="rate-list"),
    path("convert/", ConvertView.as_view(), name="convert"),
]
