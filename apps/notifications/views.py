from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


# 1. 미확인 알림 리스트 확인 API
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 요청을 보낸 유저의 알림 중 읽지 않은(is_read=False) 알림만 필터링
        return Notification.objects.filter(user=self.request.user, is_read=False)


# 2. 알림 읽기 기능을 수행하는 API
class NotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: NotificationSerializer},  # ✅ Swagger에게 응답 형태 알려주기
        description="특정 알림을 읽음 처리합니다.",
    )
    def post(self, request, pk):
        # URL Parameter로 받은 pk를 통해 해당 유저의 알림을 찾음
        notification = get_object_or_404(Notification, pk=pk, user=request.user)

        # 읽음 여부 필드를 True로 변경 후 저장
        notification.is_read = True
        notification.save()

        return Response({"message": "알림을 확인했습니다."}, status=status.HTTP_200_OK)
