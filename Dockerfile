# 베이스 이미지
FROM python:3.12-slim

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# uv가 설치되는 경로를 환경변수에 추가
ENV PATH="/root/.local/bin:${PATH}"

# 필수 패키지 설치
RUN apt-get update && apt-get install -y curl build-essential libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

# uv 설치
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY pyproject.toml uv.lock ./
# --frozen을 써서 lock 파일과 일치하게 설치, --no-install-project로 소스 전 의존성만 먼저 설치(캐싱)
RUN uv sync --frozen

# [수정] 애플리케이션 코드 전체 복사 (app 폴더가 아니라 현재 폴더 전체)
COPY . .

# [수정] 실행 권한 부여
RUN chmod +x scripts/run.sh

# 포트 설정
EXPOSE 8000

# [수정] CMD 대신 ENTRYPOINT와 scripts/run.sh 활용
# uv run을 통해 가상환경 내의 python과 패키지를 사용하도록 합니다.
ENTRYPOINT ["uv", "run", "scripts/run.sh"]