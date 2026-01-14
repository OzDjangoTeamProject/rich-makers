from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Account
from .serializers import AccountSerializer


class AccountListCreateView(generics.ListCreateAPIView):
    """
    [계좌 등록 및 목록 조회]
    GET: 현재 유저의 모든 계좌 목록 조회
    POST: 새로운 계좌 등록
    """

    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 1. select_related: N+1 문제 해결
        # 2. annotate: 각 계좌 객체에 'transaction_count' 필드를 동적으로 추가
        return (
            Account.objects.select_related("user")
            .filter(user=self.request.user)
            .annotate(
                transaction_count=Count("transactions")  # 역참조 이름(related_name) 사용
            )
        )


class AccountDetailView(generics.RetrieveDestroyAPIView):
    """
    [계좌 상세 조회 및 삭제]
    GET: 특정 계좌 정보 조회
    DELETE: 계좌 삭제
    """

    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
