from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Notification

User = get_user_model()


class NotificationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_authenticate(user=self.user)

        # 테스트용 알림 생성 (읽지 않은 것 2개, 읽은 것 1개)
        self.noti1 = Notification.objects.create(user=self.user, message="미확인 알림 1")
        self.noti2 = Notification.objects.create(user=self.user, message="미확인 알림 2")
        self.noti3 = Notification.objects.create(user=self.user, message="확인된 알림", is_read=True)

    def test_get_unread_notifications(self):
        """읽지 않은 알림 목록만 가져오는지 테스트"""
        url = reverse("notification_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 읽지 않은 알림만 필터링되므로 개수는 2개여야 함
        self.assertEqual(len(response.data), 2)

    def test_mark_notification_as_read(self):
        """알림 읽음 처리 기능 테스트"""
        url = reverse("notification_read", kwargs={"pk": self.noti1.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DB에서 실제 값이 변경되었는지 확인
        self.noti1.refresh_from_db()
        self.assertTrue(self.noti1.is_read)
