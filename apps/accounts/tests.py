from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import Account

User = get_user_model()


class AccountAPITest(APITestCase):
    def setUp(self):
        # 테스트를 위한 유저 생성 및 로그인
        self.user = User.objects.create_user(username="testuser", password="password123!")
        self.client.force_authenticate(user=self.user)  # ✅ 강제 인증 설정
        self.url = "/api/accounts/"

    def test_create_account(self):
        """계좌 생성 테스트"""
        data = {"account_name": "월급 통장"}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertIn("account_number", response.data)  # 계좌번호 자동생성 확인

    def test_get_account_list(self):
        """본인 계좌 목록 조회 테스트"""
        Account.objects.create(user=self.user, account_name="통장1", account_number="111")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_account(self):
        """계좌 삭제 테스트"""
        account = Account.objects.create(user=self.user, account_name="삭제용", account_number="222")
        response = self.client.delete(f"{self.url}{account.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.count(), 0)
