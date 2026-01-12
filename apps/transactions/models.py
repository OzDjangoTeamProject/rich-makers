from django.db import models

from apps.accounts.models import Account


class TransactionHistory(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="records")
    amount = models.BigIntegerField()
    balance_after_tx = models.BigIntegerField()
    tx_detail = models.CharField(max_length=255)  # 상세내용

    # 거래 타입 (INCOME, EXPENSE)
    tx_type = models.CharField(max_length=10)

    # 결제 수단 (CASH, CARD, TRANSFER)
    payment_method = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.tx_type}] {self.tx_detail}: {self.amount}원"
