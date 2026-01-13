from rest_framework import serializers
from apps.analysis.models import Analysis


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = [
            "id",
            "user",
            "target_type",
            "period_unit",
            "start_date",
            "end_date",
            "description",
            "result_image_url",
            "updated_at",
        ]
        read_only_fields = fields
