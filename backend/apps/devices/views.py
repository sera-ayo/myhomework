from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Device
from .serializers import DeviceRegisterSerializer, DeviceSerializer


class DeviceRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeviceRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        device = Device.objects.filter(device_code=payload["device_code"]).first()
        if device and device.user_id != request.user.id:
            return Response(
                {"detail": "设备已绑定到其他用户。"},
                status=status.HTTP_409_CONFLICT,
            )

        device, _ = Device.objects.update_or_create(
            device_code=payload["device_code"],
            defaults={
                "user": request.user,
                "brand": payload.get("brand", ""),
                "model": payload.get("model", ""),
                "android_version": payload.get("android_version", ""),
            },
        )
        return Response(DeviceSerializer(device).data, status=status.HTTP_200_OK)
