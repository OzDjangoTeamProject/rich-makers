from django.conf import settings
from django.db import models


class Account(models.Model):
    """
    사용자의 자산을 관리하는 계좌 모델입니다.
    """

    # 계좌의 주인 (유저 모델과 1:N 관계)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts")

    # 계좌 별칭 (예: 월급 통장, 비상금)
    account_name = models.CharField(max_length=50, default="기본 계좌", verbose_name="계좌 별칭")

    # 계좌 번호 (중복 불가, 자동 생성)
    account_number = models.CharField(max_length=20, unique=True, verbose_name="계좌 번호")

    # 현재 잔액 (기본값 0)
    balance = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name="현재 잔액")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.account_name} ({self.account_number})"

    @staticmethod
    def generate_account_number():
        """
        랜덤하고 고유한 계좌 번호를 생성합니다 (예: 123-456789-01).
        """
        import random

        return f"{random.randint(100, 999)}-{random.randint(100000, 999999)}-{random.randint(10, 99)}"
