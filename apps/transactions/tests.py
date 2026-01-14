from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Account
from apps.transactions.models import Transaction

User = get_user_model()


class TransactionLogicTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="password123!")
        self.client.force_authenticate(user=self.user)
        self.account = Account.objects.create(user=self.user, account_name="테스트계좌", account_number="123-456")
        self.url = "/api/transactions/"

    def test_deposit_updates_balance(self):
        """입금 시 잔액 증가 테스트"""
        data = {"account": self.account.id, "amount": 10000, "transaction_type": "DEPOSIT", "description": "입금"}
        response = self.client.post(self.url, data)

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 10000)

        # ✅ 수정: 응답 데이터(문자열)를 Decimal로 변환하여 비교하거나 문자열로 비교합니다.
        self.assertEqual(Decimal(response.data["balance_after_transaction"]), 10000)

    def test_withdraw_insufficient_balance(self):
        """잔액 부족 시 출금 실패 테스트"""
        data = {"account": self.account.id, "amount": 5000, "transaction_type": "WITHDRAW"}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  #

    def test_update_transaction_recalculates_balance(self):
        """거래 수정 시 잔액 재계산 테스트"""
        # 1. 먼저 10만원 입금
        t = Transaction.objects.create(account=self.account, amount=100000, transaction_type="DEPOSIT")

        # 2. 금액을 15만원으로 수정 (PATCH)
        self.client.patch(f"{self.url}{t.id}/", {"amount": 150000})

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 150000)  # 10만 -> 15만 반영 확인

    def test_delete_transaction_restores_balance(self):
        """거래 삭제 시 잔액 복구 테스트"""
        # 1. 5만원 입금
        t = Transaction.objects.create(account=self.account, amount=50000, transaction_type="DEPOSIT")
        # 2. 삭제
        self.client.delete(f"{self.url}{t.id}/")

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 0)  # 5만 입금 내역 삭제 시 0원으로 복구 확인
