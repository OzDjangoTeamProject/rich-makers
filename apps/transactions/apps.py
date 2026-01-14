# apps/transactions/apps.py
from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # name = "transactions" 대신 전체 경로를 적어줍니다.
    name = "apps.transactions"
