from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RiskResult
from .serializers import RiskResultSerializer


class LatestRiskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = RiskResult.objects.filter(user=request.user).order_by("-date").first()
        if result is None:
            return Response({"available": False, "message": "暂无风险数据。"})
        payload = RiskResultSerializer(result).data
        payload["available"] = True
        return Response(payload)
