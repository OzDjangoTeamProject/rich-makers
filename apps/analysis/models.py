from django.conf import settings
from django.db import models

from apps.constants import ANALYSIS_ABOUT, ANALYSIS_TYPES


class Analysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="requests")

    # 분석 대상 (INCOME/EXPENSE)
    target_type = models.CharField(
        max_length=20,
        choices=ANALYSIS_ABOUT,
        verbose_name="분석 대상",
    )

    # 분석 주기 (DAILY, WEEKLY, MONTHLY)
    period_unit = models.CharField(
        max_length=10,
        choices=ANALYSIS_TYPES,
        verbose_name="분석 주기",
    )

    start_date = models.DateField()
    end_date = models.DateField()

    # 상세 설명 및 결과 이미지 URL
    description = models.TextField(blank=True)
    result_image_url = models.URLField(max_length=500, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # get_필드명_display()를 사용하면 'TOTAL_SPENDING' 대신 '총 지출'처럼 사람이 읽기 좋은 이름이 나옵니다.
        return f"{self.user.username} - {self.get_target_type_display()} ({self.get_period_unit_display()}) 분석"
