"""
Django 공통 설정 (Base Settings)

- 프로젝트의 모든 환경(Dev, Prod)에서 공통으로 사용하는 설정을 관리합니다.
- 환경별 특화 설정은 dev.py 또는 prod.py에서 상속받아 재정의합니다.
"""

import os
from datetime import timedelta
from pathlib import Path

import environ

# [경로 설정] 프로젝트 루트 디렉터리 정의
# 위치: rich-makers/config/settings/base.py -> 상위 3단계가 Root
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# [환경 변수 로드] .env 파일의 설정을 불러옵니다.
env = environ.Env(
    DEBUG=(bool, False)  # (타입, 기본값)
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# [보안 설정] 민감한 정보는 외부 환경 변수(.env)를 참조
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

ALLOWED_HOSTS = []


# [애플리케이션 정의] 용도별 앱 분리 관리
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # ✅ 필수 추가 (allauth용)
]

THIRD_APPS = [
    "rest_framework",
    "rest_framework.authtoken",  # ✅ 필수 추가 (dj-rest-auth용)
    "drf_spectacular",
    "rest_framework_simplejwt.token_blacklist",
    # 소셜 로그인 관련
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # 셀러리 관련 (THIRD_APPS로 이동 권장)
    "django_celery_beat",
    "django_celery_results",
]

OWN_APPS = [
    "apps.users",
    "apps.accounts",
    "apps.transactions",
    "apps.analysis",
    "apps.notifications",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + OWN_APPS

# ✅ 이 설정도 반드시 파일 어딘가에 있어야 합니다!
SITE_ID = 1

# 소셜 로그인 설정 (필수)
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}

# 기본 로그인 설정 유지
REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "access",
    "JWT_AUTH_REFRESH_COOKIE": "refresh",
}

# Celery Settings
CELERY_BROKER_URL = "redis://redis:6379/0"  # Redis 컨테이너 주소
CELERY_RESULT_BACKEND = "django-db"  # 결과를 DB에 저장
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Seoul"
DJANGO_CELERY_BEAT_TZ_AWARE = False


# [미들웨어 설정] 요청/응답 처리 파이프라인
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"


# [템플릿 설정] UI 렌더링 엔진 관련
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# config/settings/base.py
DATABASES = {
    "default": env.db(),
}


# [비밀번호 검증] 보안 정책 설정
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# [국제화 및 지역화] 언어 및 시간대 설정
LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True


# [DRF & Spectacular] API 문서화 자동화 설정
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
}

# JWT 상세 설정 (필요시 기간 조절 가능)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Rich Makers API",
    "DESCRIPTION": "가계부 서비스 프로젝트 API 문서입니다.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SECURITY": [
        {"BearerAuth": []},
    ],
    "COMPONENT_SPLIT_PATCH": True,
}

# Custom User Model
AUTH_USER_MODEL = "users.User"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# config/settings/base.py 하단
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# 로그인이 성공하면 어디로 보낼지 설정
LOGIN_REDIRECT_URL = "/admin/"  # 테스트를 위해 일단 어드민으로 리다이렉트
SOCIALACCOUNT_LOGIN_ON_GET = True  # 중간 확인 페이지 없이 바로 구글 로그인창을 띄움
