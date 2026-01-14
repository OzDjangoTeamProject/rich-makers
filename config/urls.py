from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.users.views import GoogleLogin  # ✅ 직접 만든 GoogleLogin API 뷰 임포트

# [문서화 관련 URL]
docs_urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    # ✅ 1. 구글 소셜 로그인 진입점 및 콜백 처리 (구글 콘솔 설정과 일치)
    # 이 설정이 있어야 http://localhost:8000/accounts/google/login/ 주소가 작동합니다.
    path("accounts/", include("allauth.urls")),
    # ✅ 2. REST API 전용 인증 (Swagger에서 확인 가능)
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/auth/google/login/", GoogleLogin.as_view(), name="google_login"),
    # 3. 비즈니스 로직 앱 API
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/users/", include("apps.users.urls")),
    path("api/transactions/", include("apps.transactions.urls")),
    path("api/analysis/", include("apps.analysis.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
] + docs_urlpatterns

# 미디어 파일 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
