# apps/users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, LogoutView, RegisterView, UserProfileView

urlpatterns = [
    # 설계도대로 주소를 설정해: api/users/signup/
    # (이미 config/urls.py에서 api/users/까지 연결할 거라 여기선 signup/만 적어)
    path("signup/", RegisterView.as_view(), name="user_signup"),
    path("login/", LoginView.as_view(), name="user_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="user_logout"),
    path("me/", UserProfileView.as_view(), name="user_profile"),
]
