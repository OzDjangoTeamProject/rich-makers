from django.urls import path

from .views import AccountDetailView, AccountListCreateView

urlpatterns = [
    path("", AccountListCreateView.as_view(), name="account_list_create"),
    path("<int:pk>/", AccountDetailView.as_view(), name="account_detail"),
]
