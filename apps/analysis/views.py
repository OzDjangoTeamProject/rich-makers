from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .analyzers import FinanceAnalyzer  # 지난 단계에서 만든 분석기
from .models import Analysis
from .serializers import AnalysisSerializer


class AnalysisListCreateView(generics.ListCreateAPIView):
    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 로그인한 유저의 분석 내역만 조회
        return Analysis.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # 1. 요청 데이터 받기
        start_date = request.data.get("period_start")
        end_date = request.data.get("period_end")
        about = request.data.get("about", "총 지출")
        p_type = request.data.get("type", "매일")

        if not start_date or not end_date:
            return Response({"error": "시작일과 종료일을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 2. 분석기 실행
        analyzer = FinanceAnalyzer(request.user, start_date, end_date)
        analysis_obj = analyzer.generate_analysis(about_type=about, period_type=p_type)

        if not analysis_obj:
            return Response({"message": "해당 기간에 분석할 거래 내역이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 3. 결과 반환
        serializer = self.get_serializer(analysis_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
