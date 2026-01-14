from django.db.models import Q, Sum
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionListCreateView(generics.ListCreateAPIView):
    """
    [거래 내역 조회 및 생성]
    GET: 현재 유저가 소유한 모든 계좌의 거래 내역 조회
    POST: 새로운 거래(입출금) 생성
    """

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 현재 로그인한 사용자의 계좌와 연결된 거래 내역만 필터링하여 반환합니다.
        return Transaction.objects.filter(account__user=self.request.user)

    # ✅ Swagger 문서 상세화
    @extend_schema(
        summary="거래 내역 조회 및 생성",
        description="사용자가 소유한 모든 계좌의 거래 내역을 조회하거나 새로운 거래를 기록합니다.",
        responses={201: TransactionSerializer},
        examples=[
            OpenApiExample(
                "입금 예시",
                value={"account": 1, "amount": 50000, "transaction_type": "DEPOSIT", "description": "용돈"},
                request_only=True,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @extend_schema(summary="내 거래 내역 목록 조회")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    [거래 상세 조회, 수정, 삭제]
    GET: 특정 거래 상세 정보 조회
    PATCH/PUT: 거래 정보 수정 (주의: 잔액 로직 재계산 필요)
    DELETE: 거래 내역 삭제
    """

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(account__user=self.request.user)


class TransactionStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Q를 직접 임포트했다면 models.Q가 아니라 그냥 Q라고 쓰면 됩니다.
        stats = Transaction.objects.filter(account__user=request.user).aggregate(
            total_income=Sum("amount", filter=Q(transaction_type="DEPOSIT")),
            total_expenditure=Sum("amount", filter=Q(transaction_type="WITHDRAW")),
        )

        income = stats["total_income"] or 0
        expenditure = stats["total_expenditure"] or 0

        return Response({"total_income": income, "total_expenditure": expenditure, "net_amount": income - expenditure})
