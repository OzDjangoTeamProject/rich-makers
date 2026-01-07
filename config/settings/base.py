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
]

THIRD_APPS = [
    "rest_framework",
    "drf_spectacular",
]

OWN_APPS = [
    # 향후 추가될 비즈니스 로직 앱들
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + OWN_APPS


# [미들웨어 설정] 요청/응답 처리 파이프라인
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rich_makers',          # .env의 POSTGRES_DB와 일치해야 함
        'USER': 'postgres',          # .env의 POSTGRES_USER와 일치해야 함
        'PASSWORD': 'password123',   # 본인이 설정한 비밀번호
        'HOST': 'db',                # docker-compose의 서비스 이름
        'PORT': '5432',
    }
}


# [비밀번호 검증] 보안 정책 설정
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
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
