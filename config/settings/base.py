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

# [Django 기본 앱 목록] (프로젝트의 핵심 기능 제공)
DJANGO_APPS = [
    "django.contrib.admin",            # 관리자 사이트
    "django.contrib.auth",             # 인증 및 권한 관리
    "django.contrib.contenttypes",     # ContentType 프레임워크 (모델 간 관계)
    "django.contrib.sessions",         # 세션 관리
    "django.contrib.messages",         # 메시지 프레임워크 (알림 등)
    "django.contrib.staticfiles",      # 정적 파일(이미지, CSS, JS) 관리
    "django.contrib.sites",            # 사이트 프레임워크 (django-allauth에서 필요)
]

# [서드파티 앱 목록] 프로젝트에서 사용하는 외부 라이브러리 기반 앱을 나열합니다.
THIRD_APPS = [
    "rest_framework",  # Django REST Framework (API 개발)
    "drf_spectacular",  # OpenAPI 및 Swagger 문서화 도구
    "allauth",  # 사용자 인증/회원가입 프레임워크 (코어)
    "allauth.account",  # allauth의 일반 계정 기능
    "allauth.socialaccount",  # allauth의 소셜 로그인 기능 
    "allauth.socialaccount.providers.naver",  # 네이버 소셜 로그인 프로바이더
]

# [프로젝트 자체 앱 목록] 직접 개발한 앱들을 여기에 추가합니다.
OWN_APPS = [

]


INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + OWN_APPS



# [인증 백엔드] django-allauth 인증 백엔드 추가
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# [django-allauth 설정]
ACCOUNT_AUTHENTICATION_METHOD = "email"  # "email": 이메일로 로그인. "username": 사용자명으로 로그인. "username_email": 둘 다 허용.
ACCOUNT_EMAIL_REQUIRED = True            # True: 이메일 필수 입력, False: 이메일 없이도 가입 가능
ACCOUNT_UNIQUE_EMAIL = True              # 이메일 중복 가입 불가
ACCOUNT_USERNAME_REQUIRED = True         # True: username 필수 (AbstractUser 기반이면 True), False: 커스텀 유저 사용 시 username 없이도 가입 가능
ACCOUNT_EMAIL_VERIFICATION = "optional"  # "mandatory": 반드시 이메일 인증 필요, "optional": 선택, "none": 이메일 인증 안함

# [소셜 로그인 설정]
SOCIALACCOUNT_AUTO_SIGNUP = True            # True: 소셜 로그인 시 자동 회원가입, False: 추가 회원가입 절차 필요
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"   # 소셜 로그인은 이메일 인증 생략 ("none", "optional", "mandatory" 가능)
SOCIALACCOUNT_QUERY_EMAIL = True            # 소셜 프로바이더에서 이메일 정보 요청 (True 필수)

# [로그인/회원가입/로그아웃 후 리다이렉트 설정]
LOGIN_REDIRECT_URL = "/"                # 일반 로그인 후 이동할 URL
ACCOUNT_LOGIN_REDIRECT_URL = "/"        # allauth 로그인 후 이동할 URL
ACCOUNT_SIGNUP_REDIRECT_URL = "/"       # 회원가입 후 이동할 URL
ACCOUNT_LOGOUT_REDIRECT_URL = "/"       # 로그아웃 후 이동할 URL
ACCOUNT_LOGOUT_ON_GET = True            # 로그아웃 링크(GET)도 허용 (POST가 기본값)

SITE_ID = 1                             # django.contrib.sites에서 사용하는 Site의 기본 pk(1번 사이트)


# [소셜 로그인 프로바이더 세부 설정] Naver 소셜 로그인 설정
SOCIALACCOUNT_PROVIDERS = {
    "naver": {
        "APP": {
            # 네이버 애플리케이션의 client_id와 secret은 환경 변수에서 로드
            "client_id": env("NAVER_CLIENT_ID", default=""),
            "secret": env("NAVER_SECRET", default=""),
            # key는 사용하지 않으므로 빈 문자열로 설정
            "key": "",
        },
    },
}

# [미들웨어 설정] 요청/응답 처리 파이프라인
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",               # 각종 보안 기능 제공 (SSL, 보안 헤더 등)
    "django.contrib.sessions.middleware.SessionMiddleware",        # 세션 관리 (쿠키 기반 세션 지원)
    "django.middleware.common.CommonMiddleware",                   # URL 정규화, 다양한 일반적인 미들웨어 기능 제공
    "django.middleware.csrf.CsrfViewMiddleware",                  # CSRF(크로스 사이트 요청 위조) 방어
    "django.contrib.auth.middleware.AuthenticationMiddleware",     # 사용자 인증(로그인 상태) 관리
    "django.contrib.messages.middleware.MessageMiddleware",        # 뷰와 템플릿 간 메시지 전송
    "django.middleware.clickjacking.XFrameOptionsMiddleware",      # 클릭재킹 방지(X-Frame-Options 헤더 추가)
    "allauth.account.middleware.AccountMiddleware",                # allauth 관련 세션 정보 보강
]

# 프로젝트의 URL 설정이 정의된 모듈의 경로를 지정합니다.
ROOT_URLCONF = "config.urls"


# [템플릿 설정] UI 렌더링 엔진 관련
TEMPLATES = [
    {
        # 템플릿 백엔드로 DjangoTemplates 사용 (Django 기본 엔진)
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # 템플릿 디렉토리 경로 리스트 (여기에 사용자 정의 템플릿 경로 추가 가능) 
        "DIRS": [],
        # 앱 내의 templates 폴더를 자동으로 탐색
        "APP_DIRS": True,
        # 템플릿 옵션 - 컨텍스트 프로세서 등
        "OPTIONS": {
            "context_processors": [
                # request 객체를 템플릿에서 바로 사용할 수 있도록 추가
                "django.template.context_processors.request",
                # auth 관련 변수(user 등)를 템플릿에서 사용할 수 있도록 추가
                "django.contrib.auth.context_processors.auth",
                # 메시지 프레임워크 메시지를 템플릿에서 사용할 수 있도록 추가
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI 어플리케이션 경로 설정 (Django의 기본 웹서버용 인터페이스)
WSGI_APPLICATION = "config.wsgi.application"


# config/settings/base.py
DATABASES = {
    "default": env.db(),
}




# [비밀번호 검증 정책] 사용자 비밀번호의 강력함을 보장하기 위한 검증기 목록
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # 사용자 속성과 비밀번호 유사성 검사
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",            # 최소 길이 검사 (기본 8자 이상)
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",           # 자주 사용하는(쉬운) 비밀번호 금지
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",          # 숫자로만 이루어진 비밀번호 금지
    },
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
