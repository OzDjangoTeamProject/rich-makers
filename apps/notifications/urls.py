from django.urls import path
from apps.notifications.views import UnreadNotificationListView, NotificationReadView

urlpatterns = [
    path("notifications/unread/", UnreadNotificationListView.as_view(), name="notification-unread-list"),
    path("notifications/<int:pk>/read/", NotificationReadView.as_view(), name="notification-read"),
]
