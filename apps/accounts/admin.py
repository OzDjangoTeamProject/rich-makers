# apps/accounts/admin.py
from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("account_name", "account_number", "user", "balance", "created_at")
    search_fields = ("account_number", "account_name", "user__username")
