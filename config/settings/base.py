"""
Django 공통 설정 (Base Settings)

- 프로젝트의 모든 환경(Dev, Prod)에서 공통으로 사용하는 설정을 관리합니다.
- 환경별 특화 설정은 dev.py 또는 prod.py에서 상속받아 재정의합니다.
"""

import os
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
    "django.contrib.sites",  # django-allauth에서 필요
]

THIRD_APPS = [
    "rest_framework",
    "drf_spectacular",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.kakao",
    "allauth.socialaccount.providers.naver",
]

OWN_APPS = [
    #"users",
    #"accounts",
    #"transactions",
    #"analysis",
    #"notifications",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + OWN_APPS

# [인증 설정] 커스텀 User 모델 지정
#AUTH_USER_MODEL = "users.User"

# [인증 백엔드] django-allauth 인증 백엔드 추가
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# [django-allauth 설정]
ACCOUNT_AUTHENTICATION_METHOD = "email"  # 이메일 또는 사용자명으로 로그인 가능
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True  # AbstractUser 사용으로 username 필수
ACCOUNT_EMAIL_VERIFICATION = "optional"  # 이메일 인증은 선택사항

# [소셜 로그인 설정] 인증만 수행 (자동 회원가입, 이메일만 요청)
SOCIALACCOUNT_AUTO_SIGNUP = True  # 소셜 로그인 시 자동 회원가입 (인증만 수행)
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"  # 소셜 로그인은 이메일 인증 생략
SOCIALACCOUNT_QUERY_EMAIL = True  # 이메일 정보만 요청

# [로그인 후 리다이렉트 설정] 프로필 기능 없음, 루트로 리다이렉트
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGIN_REDIRECT_URL = "/"
ACCOUNT_SIGNUP_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"
# 로그아웃 시 GET 요청 허용
ACCOUNT_LOGOUT_ON_GET = True

SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env("GOOGLE_CLIENT_ID", default=""),
            "secret": env("GOOGLE_SECRET", default=""),
            "key": "",
        },
        "SCOPE": [
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
    "kakao": {
        "APP": {
            "client_id": env("KAKAO_CLIENT_ID", default=""),
            "secret": env("KAKAO_SECRET", default=""),
            "key": "",
        },
    },
    "naver": {
        "APP": {
            "client_id": env("NAVER_CLIENT_ID", default=""),
            "secret": env("NAVER_SECRET", default=""),
            "key": "",
        },
    },
}

# [미들웨어 설정] 요청/응답 처리 파이프라인
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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


# [정적 파일] CSS, JS, Images 경로 설정
STATIC_URL = "static/"


# [DRF & Spectacular] API 문서화 자동화 설정
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Rich Makers API",
    "DESCRIPTION": "가계부 서비스 프로젝트 API 문서입니다.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
