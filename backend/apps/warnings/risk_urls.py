from django.urls import path

from .risk_views import LatestRiskView


urlpatterns = [
    path("latest", LatestRiskView.as_view(), name="risk-latest"),
]
