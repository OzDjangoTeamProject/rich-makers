from django.db import models
from django.conf import settings


class Analysis(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='requests'
    )

    # 분석 대상 (INCOME/EXPENSE)
    target_type = models.CharField(max_length=10)

    # 분석 주기 (DAILY, WEEKLY, MONTHLY)
    period_unit = models.CharField(max_length=10)

    start_date = models.DateField()
    end_date = models.DateField()

    # 상세 설명 및 결과 이미지 URL
    description = models.TextField(blank=True)
    result_image_url = models.URLField(max_length=500, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.target_type} ({self.period_unit}) 분석"