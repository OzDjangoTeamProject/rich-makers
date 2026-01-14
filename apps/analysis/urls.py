from django.urls import path

from .views import AnalysisListCreateView

urlpatterns = [
    path("", AnalysisListCreateView.as_view(), name="analysis_list_create"),
]
