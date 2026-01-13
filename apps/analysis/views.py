from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.analysis.models import Analysis
from apps.analysis.serializers import AnalysisSerializer


class AnalysisListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnalysisSerializer

    def get_queryset(self):
        user = self.request.user
        period = self.request.query_params.get("period")  # weekly, monthly 등

        qs = Analysis.objects.filter(user=user).order_by("-updated_at")

        if period:
            qs = qs.filter(period_unit__iexact=period.upper())

        return qs
