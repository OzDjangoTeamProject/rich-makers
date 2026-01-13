from datetime import date
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from apps.analysis.models import Analysis

User = get_user_model()


class AnalysisListAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")

        # 분석 데이터 2개 생성
        Analysis.objects.create(
            user=self.user,
            target_type="EXPENSE",
            period_unit="DAILY",
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 31),
            description="daily test",
            result_image_url="daily.png",
        )

        Analysis.objects.create(
            user=self.user,
            target_type="EXPENSE",
            period_unit="MONTHLY",
            start_date=date(2025, 1, 1),
            end_date=date(2025, 3, 1),
            description="monthly test",
            result_image_url="monthly.png",
        )

    def test_get_all_analysis(self):
        url = reverse("analysis-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_by_period(self):
        url = reverse("analysis-list")

        response = self.client.get(url, {"period": "monthly"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["period_unit"], "MONTHLY")
