from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/common/", include("apps.common.urls")),
    path("api/auth/", include("apps.users.urls")),
    path("api/devices/", include("apps.devices.urls")),
    path("api/usage/", include("apps.usage.urls")),
    path("api/dashboard/", include("apps.analysis.urls")),
    path("api/experiments/", include("apps.analysis.experiment_urls")),
    path("api/risk/", include("apps.warnings.risk_urls")),
    path("api/warnings/", include("apps.warnings.urls")),
]
