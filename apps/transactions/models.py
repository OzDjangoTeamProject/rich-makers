from django.db import models, transaction
from rest_framework.exceptions import ValidationError

from apps.accounts.models import Account  #


class Transaction(models.Model):
    """
    계좌의 입출금 내역을 기록하는 모델입니다.
    """

    TRANSACTION_TYPE_CHOICES = [
        ("DEPOSIT", "입금"),
        ("WITHDRAW", "출금"),
    ]

    # 연결된 계좌
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")

    # 거래 금액
    amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="거래 금액")

    # 거래 유형 (입금/출금)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, verbose_name="거래 유형")

    # 거래 후 잔액 (나중에 내역을 조회할 때 당시 잔액을 알기 위함)
    balance_after_transaction = models.DecimalField(max_digits=15, decimal_places=0, verbose_name="거래 후 잔액")

    # 거래 내용 (예: 편의점, 월급)
    description = models.CharField(max_length=255, blank=True, verbose_name="거래 내용")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # 최신 거래가 위로 오도록 설정

    def __str__(self):
        return f"{self.account.account_name} - {self.transaction_type} ({self.amount})"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            account = self.account
            if not self.pk:  # 🆕 신규 생성
                if self.transaction_type == "DEPOSIT":
                    account.balance += self.amount
                else:
                    if account.balance < self.amount:
                        raise ValidationError("잔액이 부족합니다.")
                    account.balance -= self.amount
            else:  # 🔄 기존 내역 수정 (어드민/API 공통)
                old_instance = Transaction.objects.get(pk=self.pk)
                # 1. 기존 금액 롤백
                if old_instance.transaction_type == "DEPOSIT":
                    account.balance -= old_instance.amount
                else:
                    account.balance += old_instance.amount
                # 2. 새로운 금액 적용
                if self.transaction_type == "DEPOSIT":
                    account.balance += self.amount
                else:
                    if account.balance < self.amount:
                        raise ValidationError("잔액이 부족합니다.")
                    account.balance -= self.amount

            account.save()
            self.balance_after_transaction = account.balance
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):  # 🔙 삭제 로직
        with transaction.atomic():
            account = self.account
            if self.transaction_type == "DEPOSIT":
                account.balance -= self.amount
            else:
                account.balance += self.amount
            account.save()
            super().delete(*args, **kwargs)
