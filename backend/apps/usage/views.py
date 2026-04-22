from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BulkUsageUploadSerializer
from .services import ingest_usage_sessions


class BulkUsageSessionUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BulkUsageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = ingest_usage_sessions(user=request.user, payload=serializer.validated_data)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "created_count": result["created_count"],
                "duplicate_count": result["duplicate_count"],
                "processed_dates": result["processed_dates"],
                "last_sync_at": result["device"].last_sync_at,
            },
            status=status.HTTP_200_OK,
        )
