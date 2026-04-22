from django.urls import path

from .views import (
    DashboardCategoriesView,
    DashboardSummaryView,
    DashboardTrendView,
)


urlpatterns = [
    path("summary", DashboardSummaryView.as_view(), name="dashboard-summary"),
    path("trend", DashboardTrendView.as_view(), name="dashboard-trend"),
    path("categories", DashboardCategoriesView.as_view(), name="dashboard-categories"),
]
