# apps/notifications/tests/test_notification_api.py

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.notifications.models import Notification

User = get_user_model()


class NotificationAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # ⚠️ email이 UNIQUE라서 반드시 서로 다른 email을 넣어야 함
        cls.user = User.objects.create_user(
            username="u1",
            email="u1@example.com",
            password="pass1234",
        )
        cls.other = User.objects.create_user(
            username="u2",
            email="u2@example.com",
            password="pass1234",
        )

        # 내 알림 2개: unread 1개, read 1개
        cls.my_unread = Notification.objects.create(user=cls.user, message="안읽은 알림", is_read=False)
        cls.my_read = Notification.objects.create(user=cls.user, message="읽은 알림", is_read=True)

        # 다른 사람 알림
        cls.other_unread = Notification.objects.create(user=cls.other, message="남의 알림", is_read=False)

        # urls.py에서 name을 지정했다면 reverse로 안전하게 호출
        cls.unread_url = reverse("notification-unread-list")
        cls.read_url = reverse("notification-read", kwargs={"pk": cls.my_unread.pk})
        cls.other_read_url = reverse("notification-read", kwargs={"pk": cls.other_unread.pk})

    # ---------- Unread List ----------

    def test_unread_list_requires_authentication(self):
        res = self.client.get(self.unread_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unread_list_returns_only_my_unread(self):
        self.client.login(username="u1", password="pass1234")

        res = self.client.get(self.unread_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # 응답이 리스트라고 가정
        returned_ids = [item["id"] for item in res.data]

        self.assertIn(self.my_unread.id, returned_ids)          # 내 unread 포함
        self.assertNotIn(self.my_read.id, returned_ids)         # 내 read 제외
        self.assertNotIn(self.other_unread.id, returned_ids)    # 남의 알림 제외

        # unread만 내려오는지 추가 검증
        for item in res.data:
            self.assertFalse(item["is_read"])

    # ---------- Mark Read ----------

    def test_mark_read_requires_authentication(self):
        res = self.client.patch(self.read_url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_mark_read_success(self):
        self.client.login(username="u1", password="pass1234")

        # 처음엔 unread
        self.my_unread.refresh_from_db()
        self.assertFalse(self.my_unread.is_read)

        res = self.client.patch(self.read_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.my_unread.refresh_from_db()
        self.assertTrue(self.my_unread.is_read)

    def test_cannot_mark_other_users_notification(self):
        self.client.login(username="u1", password="pass1234")

        res = self.client.patch(self.other_read_url)

        # get_object_or_404(pk=pk, user=request.user) 패턴이면 404가 정답
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
