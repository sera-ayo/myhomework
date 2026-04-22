from django.conf import settings
from django.db import models


class Device(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="devices",
    )
    device_code = models.CharField(max_length=128, unique=True)
    brand = models.CharField(max_length=64, blank=True)
    model = models.CharField(max_length=64, blank=True)
    android_version = models.CharField(max_length=32, blank=True)
    last_sync_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"{self.device_code} ({self.user})"
