import os

from .base import *  # noqa: F403

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",  # 개발 서버 바인딩 때문에 들어오는 경우 대비
    "web",  # docker-compose 서비스명(컨테이너 간 호출용)
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# 데이터베이스 엔진 설정 (ImproperlyConfigured 에러 해결책)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),  #
        "USER": os.environ.get("POSTGRES_USER"),  #
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),  #
        "HOST": os.environ.get("DJANGO_DB_HOST", "db"),  # 도커 서비스 이름 'db'
        "PORT": os.environ.get("DJANGO_DB_PORT", "5432"),  #
    }
}

DEBUG = True
