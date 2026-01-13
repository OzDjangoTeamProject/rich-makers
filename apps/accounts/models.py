from django.conf import settings
from django.db import models

from apps.constants import BANK_CODES


class Account(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="possesses",
        db_index=True,
    )
    account_number = models.CharField(max_length=30)

    # constants.py의 리스트를 choices로 연결
    bank_code = models.CharField(max_length=10, choices=BANK_CODES, verbose_name="은행")

    account_type = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - {self.get_bank_code_display()} ({self.account_number})"
