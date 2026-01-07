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
