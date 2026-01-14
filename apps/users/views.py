# apps/users/views.py
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UserProfileSerializer, UserSignupSerializer  # 만든 시리얼라이저


class RegisterView(generics.CreateAPIView):
    """
    회원가입을 처리하는 뷰,
    CreateAPIView는 POST 요청을 받아 새로운 데이터를 생성하는 데 최적화.
    """

    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    # 회원가입은 로그인하지 않은 사용자도 할 수 있어야 하니 누구나 접근 허용!
    permission_classes = [AllowAny]


class LoginView(TokenObtainPairView):
    """
    [3단계 미션3] 로그인 API
    아이디와 비밀번호를 받아서 액세스 토큰과 리프레시 토큰을 발급합니다.
    """

    permission_classes = [AllowAny]


class LogoutView(APIView):
    """
    [3단계 미션4] 로그아웃 API
    전달받은 Refresh Token을 블랙리스트에 추가하여 무효화합니다.
    """

    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능

    @extend_schema(
        summary="로그아웃",
        description="Refresh Token을 받아 블랙리스트에 등록합니다.",
        request={
            "application/json": {
                "type": "object",
                "properties": {"refresh": {"type": "string", "help_text": "무효화할 리프레시 토큰"}},
                "required": ["refresh"],
            }
        },
        responses={200: OpenApiResponse(description="성공")},
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # ✅ 토큰 블랙리스트 처리

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    [미션] 유저 정보 확인(GET), 수정(PATCH), 삭제(DELETE) API
    """

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  # 로그인한 사람만 접근 가능

    def get_object(self):
        # URL에서 pk를 받지 않고, 현재 로그인한 사용자의 정보를 바로 반환해.
        # 이렇게 하면 /api/users/me/ 주소 하나로 본인 정보만 안전하게 관리할 수 있어!
        return self.request.user


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/api/auth/google/login/callback/"  # ✅ 구글 콘솔 설정과 일치
    client_class = OAuth2Client
