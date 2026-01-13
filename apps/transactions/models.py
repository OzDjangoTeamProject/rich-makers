from django.core.exceptions import ValidationError
from django.db import models, transaction

from apps.accounts.models import Account
from apps.constants import TRANSACTION_CATEGORY


class TransactionHistory(models.Model):
    """
    거래 내역 기록 및 계좌 잔액 자동 업데이트 모델
    """

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="records", verbose_name="연결된 계좌")
    amount = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="거래 금액")
    balance_after_tx = models.DecimalField(max_digits=20, decimal_places=2, editable=False, verbose_name="거래 후 잔액")
    tx_detail = models.CharField(max_length=255, verbose_name="거래 상세 내용")
    category = models.CharField(max_length=20, choices=TRANSACTION_CATEGORY, default="ETC", verbose_name="카테고리")
    tx_type = models.CharField(max_length=10, verbose_name="거래 타입")  # DEPOSIT / WITHDRAW
    payment_method = models.CharField(max_length=15, verbose_name="결제 수단")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="거래 일시")

    @transaction.atomic
    def save(self, *args, **kwargs):
        # 1. DB에서 계좌 정보를 가져오며 잠금(Lock)
        account = Account.objects.select_for_update().get(pk=self.account.pk)

        # 2. 새로운 거래 생성 시 잔액 계산
        if not self.pk:
            if self.tx_type == "DEPOSIT":
                account.balance += self.amount
            elif self.tx_type == "WITHDRAW":
                if account.balance < self.amount:
                    raise ValidationError("계좌 잔액이 부족합니다.")
                account.balance -= self.amount

            # 계좌 잔액 업데이트 후 저장
            account.save()
            # 현재 거래 내역에 '계산된 잔액' 기록
            self.balance_after_tx = account.balance

        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.tx_type}] {self.tx_detail} ({self.amount}원)"
