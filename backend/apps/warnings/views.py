from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WarningRecord
from .serializers import WarningRecordSerializer


class WarningListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = WarningRecord.objects.filter(user=request.user).order_by("-warning_time")[:30]
        return Response({"items": WarningRecordSerializer(records, many=True).data})
