from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase  # ✅ TestCase 대신 APITestCase 사용

from apps.accounts.models import Account
from apps.analysis.analyzers import FinanceAnalyzer
from apps.analysis.models import Analysis
from apps.transactions.models import Transaction

User = get_user_model()


class AnalyzerTest(APITestCase):  # ✅ APITestCase로 변경
    def setUp(self):
        # 1. 테스트용 유저 생성
        self.user = User.objects.create_user(username="testuser", password="password123")

        # ✅ DRF API 테스트를 위해 클라이언트에 유저 인증 강제 적용
        self.client.force_authenticate(user=self.user)

        # 2. Account 생성
        self.account = Account.objects.create(
            user=self.user,
            account_name="테스트계좌",
            account_number=Account.generate_account_number(),
            balance=100000,
        )

        # 3. 분석 대상 데이터(출금) 생성
        Transaction.objects.create(account=self.account, amount=5000, transaction_type="WITHDRAW", description="커피")

    def test_analyzer_generates_image(self):
        """분석기가 데이터를 정상적으로 읽고 이미지 파일을 생성하는지 테스트"""
        analyzer = FinanceAnalyzer(self.user, date(2026, 1, 1), date(2026, 1, 31))
        analysis_obj = analyzer.generate_analysis()

        self.assertIsNotNone(analysis_obj)
        self.assertTrue(bool(analysis_obj.result_image))
        self.assertEqual(analysis_obj.about, "지출 통계")

    def test_analysis_list_view(self):
        """작성된 분석 결과 목록을 정상적으로 가져오는지 테스트"""
        # 1. 테스트용 분석 데이터 2개 생성
        Analysis.objects.create(user=self.user, about="분석1", type="매일")
        Analysis.objects.create(user=self.user, about="분석2", type="매주")

        # 2. API 엔드포인트에 GET 요청
        url = reverse("analysis_list_create")
        response = self.client.get(url)

        # 3. 검증 (이제 200 OK가 떨어집니다)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # 💡 API 응답 순서에 따라 '분석1' 위치가 다를 수 있으므로 포함 여부로 체크하는 것이 안전합니다.
        self.assertTrue(any(item["about"] == "분석1" for item in response.data))
