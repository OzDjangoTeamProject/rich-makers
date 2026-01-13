from django.urls import path
from apps.analysis.views import AnalysisListView

urlpatterns = [
    path("", AnalysisListView.as_view(), name="analysis-list"),
]
