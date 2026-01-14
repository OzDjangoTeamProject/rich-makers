import os
from io import BytesIO

import matplotlib

matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
from django.core.files.base import ContentFile

from apps.transactions.models import Transaction

from .models import Analysis


# ✅ 폰트 설정 로직을 함수화하여 안전하게 호출합니다.
def get_korean_font():
    """시스템 내 나눔고딕 폰트 확인 및 설정"""
    # 1. 보편적인 리눅스 폰트 경로 확인
    path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
    if os.path.exists(path):
        return fm.FontProperties(fname=path)

    # 2. 시스템 폰트 목록에서 이름으로 확인
    font_names = [f.name for f in fm.fontManager.ttflist]
    if "NanumGothic" in font_names:
        return fm.FontProperties(family="NanumGothic")

    return None


# 전역 폰트 프로퍼티 설정
FONT_PROP = get_korean_font()
if FONT_PROP:
    plt.rc("font", family=FONT_PROP.get_name())
plt.rcParams["axes.unicode_minus"] = False


class FinanceAnalyzer:
    def __init__(self, user, start_date, end_date):
        self.user = user
        self.start_date = start_date
        self.end_date = end_date

    def get_data(self):
        qs = Transaction.objects.filter(
            account__user=self.user, created_at__date__range=[self.start_date, self.end_date]
        ).values("created_at__date", "amount", "transaction_type")
        return pd.DataFrame(list(qs))

    def generate_analysis(self, about_type="지출 통계", period_type="매일"):
        df = self.get_data()
        if df.empty:
            return None

        df["amount"] = df["amount"].astype(float)
        withdrawals = df[df["transaction_type"] == "WITHDRAW"].copy()
        if withdrawals.empty:
            return None

        summary = withdrawals.groupby("created_at__date")["amount"].sum()

        plt.style.use("seaborn-v0_8-muted")
        fig, ax = plt.subplots(figsize=(12, 6))

        bars = summary.plot(kind="bar", color="#5DADE2", edgecolor="white", ax=ax)

        # ✅ 폰트 프로퍼티가 있을 때만 적용하여 에러를 방지합니다.
        title_font = {"fontproperties": FONT_PROP} if FONT_PROP else {}

        plt.title(f"📊 {about_type} ({self.start_date} ~ {self.end_date})", fontsize=16, pad=20, **title_font)
        plt.xlabel("날짜", fontsize=12, **title_font)
        plt.ylabel("금액 (원)", fontsize=12, **title_font)

        for bar in bars.patches:
            ax.annotate(
                f"{int(bar.get_height()):,}원",
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                ha="center",
                va="bottom",
                fontsize=10,
                xytext=(0, 5),
                textcoords="offset points",
                **title_font,
            )

        plt.xticks(rotation=45, **title_font)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format="png", dpi=100)
        plt.close()

        buffer.seek(0)
        filename = f"analysis_{self.user.id}_{self.start_date}.png"

        analysis = Analysis.objects.create(
            user=self.user,
            about=about_type,
            type=period_type,
            period_start=self.start_date,
            period_end=self.end_date,
            description=f"{self.start_date}부터 {self.end_date}까지의 지출 분석 결과입니다.",
        )

        analysis.result_image.save(filename, ContentFile(buffer.read()), save=True)
        return analysis
