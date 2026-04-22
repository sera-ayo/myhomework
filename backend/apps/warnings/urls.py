from django.urls import path

from .views import WarningListView


urlpatterns = [
    path("list", WarningListView.as_view(), name="warning-list"),
]
