# apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    관리자 페이지에서 유저 관리 기능을 강화합니다.
    """

    # 1. 목록에서 보여줄 필드들
    list_display = ("username", "email", "nickname", "membership_status", "is_staff", "is_active")

    # 2. ✅ 검색 기능 설정: 이메일, 닉네임, 휴대폰 번호로 검색 가능
    # 'nickname'과 'phone_number'는 우리가 추가한 필드입니다.
    search_fields = ("email", "nickname", "phone_number", "username")

    # 3. ✅ 필터링 설정: 관리자 여부(is_staff)와 계정 활성화 상태(is_active)로 필터링
    list_filter = ("is_staff", "is_active", "membership_status")

    # 4. 상세 페이지 설정
    fieldsets = UserAdmin.fieldsets + (("추가 정보", {"fields": ("nickname", "phone_number", "membership_status")}),)

    # 5. ✅ 어드민 여부(is_staff) 접근 제한 설정
    # 관리자 페이지에 들어온 모든 '관리자'가 이 값을 함부로 수정하지 못하게
    # 읽기 전용(readonly)으로 만들거나, 특정 조건에 따라 제어할 수 있습니다.
    def get_readonly_fields(self, request, obj=None):
        # 만약 현재 로그인한 사람이 슈퍼유저(최고 관리자)가 아니라면
        # 'is_staff' 필드를 수정할 수 없도록 읽기 전용으로 설정합니다.
        if not request.user.is_superuser:
            return self.readonly_fields + ("is_staff", "is_superuser")
        return self.readonly_fields
