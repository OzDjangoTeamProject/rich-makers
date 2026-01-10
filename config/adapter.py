"""
어댑터 설정 - 로그아웃 메시지 제거, 소셜 로그인 인증만 수행
기존 구조 유지하면서 설정만 변경
"""
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.generic import View


class CustomAccountAdapter(DefaultAccountAdapter):
    """로그아웃 메시지 제거하는 커스텀 어댑터"""

    def is_open_for_signup(self, request):
        """회원가입 허용"""
        return True


class LogoutView(View):
    """로그아웃 메시지 없이 로그아웃하는 커스텀 뷰"""

    def get(self, request, *args, **kwargs):
        """GET 요청으로 로그아웃 (메시지 없음)"""
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect("/")

    def post(self, request, *args, **kwargs):
        """POST 요청으로 로그아웃 (메시지 없음)"""
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect("/")


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """프로필 기능 없이 인증만 수행하는 커스텀 어댑터"""

    def get_connect_redirect_url(self, request, socialaccount):
        """소셜 계정 연결 후 리다이렉트 URL"""
        return "/"

    def is_auto_signup_allowed(self, request, sociallogin):
        """자동 회원가입 허용 (인증만 수행)"""
        return True

    def populate_user(self, request, sociallogin, data):
        """사용자 정보 채우기 - 최소한의 정보만"""
        user = super().populate_user(request, sociallogin, data)
        return user
