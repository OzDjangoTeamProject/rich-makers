from django.urls import path

from .views import TransactionDetailView, TransactionListCreateView, TransactionStatisticsView

urlpatterns = [
    path("", TransactionListCreateView.as_view(), name="transaction_list_create"),
    path("<int:pk>/", TransactionDetailView.as_view(), name="transaction_detail"),
    path("stats/", TransactionStatisticsView.as_view(), name="transaction_stats"),
]
