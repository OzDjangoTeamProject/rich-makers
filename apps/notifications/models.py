from django.conf import settings
from django.db import models


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receives")

    # 알림 내용
    message = models.TextField()

    # 읽음 처리 여부
    is_read = models.BooleanField(default=False)

    # 알림 생성 시각
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "읽음" if self.is_read else "안읽음"
        return f"[{status}] {self.user.username}님, 알림 왔어요!"
