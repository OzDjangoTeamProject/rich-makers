from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.dateparse import parse_date

from apps.analysis.analyzers import Analyzer

User = get_user_model()


@shared_task
def run_analysis_task(user_id: int, start_date: str, end_date: str):
    """
    단일 유저에 대해 Analyzer를 실행한다.
    (API / 수동 실행용)

    Args:
        user_id (int): 분석 대상 유저 ID
        start_date (str): "YYYY-MM-DD"
        end_date (str): "YYYY-MM-DD"

    Returns:
        dict: {
            "analysis_id": int,
            "result_image_url": str,
        }
    """
    user = User.objects.get(id=user_id)

    start = parse_date(start_date)
    end = parse_date(end_date)

    if not start or not end:
        raise ValueError("start_date/end_date must be YYYY-MM-DD format")

    analysis = Analyzer(
        user=user,
        start_date=start,
        end_date=end,
    ).run()

    return {
        "analysis_id": analysis.id,
        "result_image_url": analysis.result_image_url,
    }


@shared_task
def run_daily_expense_analysis_for_all_users():
    """
    모든 유저에 대해 '어제' 지출 분석을 생성한다.
    (Celery Beat 스케줄용)
    """
    today = timezone.localdate()
    start = today - timedelta(days=1)
    end = start

    created = 0

    for user in User.objects.all().iterator():
        try:
            Analyzer(
                user=user,
                start_date=start,
                end_date=end,
            ).run()
            created += 1
        except Exception:
            # 데이터 없거나 오류 발생 시 개별 유저만 스킵
            continue

    return {
        "created": created,
        "start": str(start),
        "end": str(end),
    }
