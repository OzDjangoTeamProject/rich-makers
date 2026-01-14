# apps/notifications/apps.py
from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.notifications"  # ✅ 'notifications'가 아닌 전체 경로인지 확인하세요!
