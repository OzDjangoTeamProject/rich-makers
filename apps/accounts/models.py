from django.conf import settings
from django.db import models

from apps.constants import BANK_CODES


class Account(models.Model):
    """
    사용자 계좌 모델
    - User 1 : N Account
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accounts",
    )

    account_number = models.CharField(
        max_length=30,
        null=True,        # 초기 마이그레이션 + 테스트용
        blank=True,
        verbose_name="계좌번호",
    )

    bank_code = models.CharField(
        max_length=10,
        choices=BANK_CODES,
        verbose_name="은행",
    )

    account_type = models.CharField(
        max_length=20,
        verbose_name="계좌 유형",
    )

    balance = models.BigIntegerField(
        default=0,
        verbose_name="잔액",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="생성일",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="수정일",
    )

    class Meta:
        db_table = "accounts"
        verbose_name = "계좌"
        verbose_name_plural = "계좌 목록"

    def __str__(self):
        return f"{self.user} | {self.get_bank_code_display()} | {self.account_number}"
