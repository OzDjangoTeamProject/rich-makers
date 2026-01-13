from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from unittest.mock import patch

from apps.accounts.models import Account
from apps.transactions.models import TransactionHistory
from apps.analysis.analyzers import Analyzer
from apps.analysis.models import Analysis

User = get_user_model()


class AnalyzerTest(TestCase):
    def setUp(self):
        # 유저 생성
        self.user = User.objects.create_user(username="testuser", password="password123")

        # 계좌 생성
        self.account = Account.objects.create(
            user=self.user,
            balance=100_000,
            account_number="123-456",
        )

        # 거래 1건 생성 (Analyzer가 사용하는 필드들 + NOT NULL 필드 포함)
        TransactionHistory.objects.create(
            account=self.account,
            amount=12_000,
            tx_type="EXPENSE",
            tx_detail="점심",
            payment_method="CARD",
            balance_after_tx=self.account.balance - 12_000,
            created_at=timezone.now(),
        )

    @patch("apps.analysis.analyzers.plt.savefig")
    def test_analyzer_creates_analysis_and_saves_image(self, mock_savefig):
        analyzer = Analyzer(
            user=self.user,
            start_date=date(2025, 1, 1),
            end_date=date(2026, 12, 31),
        )

        analysis = analyzer.run()

        # 1) Analysis 모델이 생성됐는지
        self.assertIsInstance(analysis, Analysis)
        self.assertEqual(analysis.user, self.user)
        self.assertEqual(analysis.target_type, "EXPENSE")
        self.assertEqual(analysis.period_unit, "CUSTOM")

        # 2) DB에 실제로 저장됐는지
        self.assertTrue(Analysis.objects.filter(id=analysis.id).exists())

        # 3) 이미지 저장(savefig)이 호출됐는지 (실제 파일 생성은 안 함)
        mock_savefig.assert_called_once()

        # 4) 결과 경로가 들어갔는지 (빈 값 아니면 OK)
        self.assertTrue(analysis.result_image_url)
