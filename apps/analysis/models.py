from django.conf import settings
from django.db import models
from django.utils import timezone  # ✅ 시간 기본값을 위해 추가


class Analysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="analyses")
    # ✅ default 값을 추가합니다.
    about = models.CharField(max_length=100, default="지출 분석", help_text="분석 내용")
    type = models.CharField(max_length=50, default="매일", help_text="분석 기간 유형")
    period_start = models.DateField(default=timezone.now, verbose_name="분석 시작일")
    period_end = models.DateField(default=timezone.now, verbose_name="분석 종료일")

    description = models.TextField(blank=True, verbose_name="데이터 분석 설명")
    result_image = models.ImageField(upload_to="analysis_results/%Y/%m/", verbose_name="분석 그래프 이미지")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.about} ({self.type})"
