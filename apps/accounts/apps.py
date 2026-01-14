# apps/accounts/apps.py
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # name = "accounts" 대신 전체 경로를 적어줍니다.
    name = "apps.accounts"
