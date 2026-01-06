#!/bin/sh
set -e

echo "--- Database Migration 시작 ---"
# makemigrations --check는 변경사항이 있는데 파일이 없을 때 에러를 냅니다.
# 개발 중에는 자동으로 만들어주는 게 편하므로 아래처럼 구성합니다.
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "--- Static 파일 수집 (선택사항) ---"
# 배포 환경을 고려한다면 추가하는 것이 좋습니다.
# python manage.py collectstatic --noinput

echo "--- Gunicorn 실행 ---"
# Dockerfile의 ENTRYPOINT에서 'uv run'을 썼으므로 여기선 gunicorn만 호출해도 됩니다.
exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application --workers 2