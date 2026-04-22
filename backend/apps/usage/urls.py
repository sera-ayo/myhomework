from django.urls import path

from .views import BulkUsageSessionUploadView


urlpatterns = [
    path("sessions/bulk", BulkUsageSessionUploadView.as_view(), name="usage-sessions-bulk"),
]
