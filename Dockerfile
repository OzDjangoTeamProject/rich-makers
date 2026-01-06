# 1. 베이스 이미지 설정 (Python 3.13)
FROM python:3.13-slim

# 2. 필수 패키지 설치 (uv 설치를 위한 curl 등)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. uv 설치 및 환경 변수 설정
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. 작업 디렉터리 설정
WORKDIR /app

# 5. 의존성 파일 복사 및 설치
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# 6. 나머지 소스 코드 복사
COPY . .

# 7. 실행 권한 부여
RUN chmod +x scripts/run.sh

# 8. 포트 개방
EXPOSE 8000

# 9. 실행 스크립트 가동 (uv 환경 내에서 실행)
ENTRYPOINT ["uv", "run", "scripts/run.sh"]