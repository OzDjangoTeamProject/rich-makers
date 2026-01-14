import os

from celery import Celery

# 장고의 기본 설정 모듈을 지정합니다.
# 개발 환경에 맞춰 config.settings.dev로 기본값을 설정하는 것이 안전합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("rich_makers")

# CELERY_로 시작하는 모든 설정값들을 장고 settings.py에서 읽어옵니다.
app.config_from_object("django.conf:settings", namespace="CELERY")

# 프로젝트 내 모든 앱 폴더에서 tasks.py 파일을 자동으로 찾아 등록합니다.
app.autodiscover_tasks()
