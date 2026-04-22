from django.urls import path

from .views import ExperimentMetricsView


urlpatterns = [
    path("metrics", ExperimentMetricsView.as_view(), name="experiment-metrics"),
]
