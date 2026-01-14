# apps/transactions/admin.py
from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    관리자 페이지에서 거래 내역을 관리합니다.
    """

    # 1. 목록에 표시할 필드들
    list_display = ("id", "account", "transaction_type", "amount", "balance_after_transaction", "created_at")

    # 2. 우측 필터 메뉴: 거래 유형과 날짜별로 필터링 가능
    list_filter = ("transaction_type", "created_at", "account")

    # 3. 검색 기능: 계좌 이름, 계좌 번호, 거래 내용으로 검색 가능
    search_fields = ("account__account_name", "account__account_number", "description")

    # 4. 정렬 방식: 최신 거래가 가장 위에 오도록 설정
    ordering = ("-created_at",)

    # 5. 읽기 전용 필드: 거래 후 잔액은 로직에 의해 계산되므로 수정을 막는 것이 좋습니다.
    readonly_fields = ("balance_after_transaction", "created_at")

    # 선택 사항: 상세 페이지에서 필드 순서 배치
    fieldsets = (
        ("기본 정보", {"fields": ("account", "transaction_type", "amount")}),
        ("추가 정보", {"fields": ("description", "balance_after_transaction", "created_at")}),
    )
