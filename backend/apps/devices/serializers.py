from rest_framework import serializers

from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            "id",
            "device_code",
            "brand",
            "model",
            "android_version",
            "last_sync_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "last_sync_at", "created_at", "updated_at"]


class DeviceRegisterSerializer(serializers.Serializer):
    device_code = serializers.CharField(max_length=128)
    brand = serializers.CharField(max_length=64, allow_blank=True, required=False)
    model = serializers.CharField(max_length=64, allow_blank=True, required=False)
    android_version = serializers.CharField(
        max_length=32,
        allow_blank=True,
        required=False,
    )
