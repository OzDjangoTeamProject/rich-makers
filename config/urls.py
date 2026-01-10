from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,  # 프로젝트의 API 설계도(Schema)를 생성합니다.
    SpectacularRedocView,  # 정적이고 깔끔한 문서 위주의 화면입니다.
    SpectacularSwaggerView,  # 브라우저에서 직접 API를 테스트(Try it out)할 수 있는 화면입니다.
)

# 문서화 관련 URL
docs_urlpatterns = [
    # Schema URL
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger URL
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Redoc URL
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]




urlpatterns = [

    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),  # 소셜 로그인 URL 패턴
] + docs_urlpatterns  # 문서화 관련 URL 합치기
