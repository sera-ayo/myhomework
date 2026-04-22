from datetime import date

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import (
    dashboard_categories_for_user,
    dashboard_summary_for_user,
    dashboard_trend_for_user,
    experiments_payload,
)


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(dashboard_summary_for_user(request.user))


class DashboardTrendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get("days", 7))
        if days not in {7, 30}:
            days = 7
        return Response({"items": dashboard_trend_for_user(request.user, days=days)})


class DashboardCategoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        raw_date = request.query_params.get("date")
        target_date = None
        if raw_date:
            target_date = date.fromisoformat(raw_date)
        return Response(dashboard_categories_for_user(request.user, day=target_date))


class ExperimentMetricsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request):
        return Response(experiments_payload())
