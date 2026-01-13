# Python 3.13 버전이 설치된 가벼운 리눅스 기반으로 시작해
FROM python:3.13.1-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# uv가 사용할 가상환경 위치를 강제로 /app/.venv로 고정
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

# run.sh가 bash를 사용하므로 bash 설치
RUN apt-get update && apt-get install -y --no-install-recommends bash \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 의존성 파일 먼저 복사 (캐시 효율)
COPY pyproject.toml uv.lock ./

# venv 생성 + prod 그룹 포함 설치
# 프로젝트에 필요한 재료들을 실제로 설치
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv /app/.venv && \
    uv sync --frozen --no-install-project --no-dev --group prod

# 빌드 단계에서 설치 검증: 여기서 django import 실패하면 빌드가 실패함
RUN /app/.venv/bin/python -c "import django; print('Django:', django.get_version())"

# 소스 코드 복사
COPY . .

RUN chmod +x scripts/run.sh

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
