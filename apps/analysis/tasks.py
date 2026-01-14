from datetime import date, timedelta

from celery import shared_task
from django.contrib.auth import get_user_model

from apps.notifications.models import Notification

from .analyzers import FinanceAnalyzer

User = get_user_model()


@shared_task
def generate_daily_analysis_for_all_users():
    today = date.today()
    yesterday = today - timedelta(days=1)
    users = User.objects.all()
    results = []

    for user in users:
        analyzer = FinanceAnalyzer(user, yesterday, yesterday)
        analysis_obj = analyzer.generate_analysis(about_type=f"{yesterday} 일일 자동 분석", period_type="매일")

        if analysis_obj:
            # ✅ 분석 성공 시 유저에게 알림 생성
            Notification.objects.create(
                user=user, message=f"📊 {yesterday}의 지출 분석 리포트가 생성되었습니다! 지금 확인해보세요."
            )
            results.append(f"Success: {user.username}")

    return results
