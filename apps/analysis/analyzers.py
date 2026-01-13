import os
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt

from django.conf import settings

from apps.transactions.models import TransactionHistory
from apps.analysis.models import Analysis


class Analyzer:
    """
    DataFrame을 시각화하여 이미지로 저장하고
    해당 결과를 Analysis 모델로 저장한다.
    """

    def __init__(self, user, start_date: date, end_date: date):
        self.user = user
        self.start_date = start_date
        self.end_date = end_date

    def get_transactions(self):
        """
        유저 + 기간 기준 지출 거래 조회
        """
        return TransactionHistory.objects.filter(
            account__user=self.user,
            created_at__date__gte=self.start_date,
            created_at__date__lte=self.end_date,
            tx_type="EXPENSE",
        ).values(
            "created_at",
            "amount",
        )

    def create_dataframe(self) -> pd.DataFrame:
        """
        QuerySet → pandas DataFrame
        """
        qs = self.get_transactions()
        df = pd.DataFrame(list(qs))

        if df.empty:
            raise ValueError("분석할 거래 데이터가 없습니다.")

        df["created_at"] = pd.to_datetime(df["created_at"])
        df["date"] = df["created_at"].dt.date

        return df

    def visualize(self, df: pd.DataFrame) -> str:
        """
        날짜별 지출 합계를 시각화하여 이미지로 저장
        """
        summary = (
            df.groupby("date")["amount"]
            .sum()
            .sort_index()
        )

        plt.figure(figsize=(8, 6))
        summary.plot(kind="bar")
        plt.title("날짜별 지출 분석")
        plt.xlabel("날짜")
        plt.ylabel("금액")
        plt.tight_layout()

        filename = f"analysis_{self.user.id}_{self.start_date}_{self.end_date}.png"
        relative_path = os.path.join("analysis", filename)
        absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)

        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
        plt.savefig(absolute_path)
        plt.close()

        return relative_path

    def save_analysis(self, image_path: str) -> Analysis:
        """
        Analysis 모델 생성
        """
        return Analysis.objects.create(
            user=self.user,
            target_type="EXPENSE",
            period_unit="CUSTOM",
            start_date=self.start_date,
            end_date=self.end_date,
            description="기간별 날짜별 지출 분석",
            result_image_url=image_path,
        )

    def run(self) -> Analysis:
        df = self.create_dataframe()
        image_path = self.visualize(df)
        return self.save_analysis(image_path)
