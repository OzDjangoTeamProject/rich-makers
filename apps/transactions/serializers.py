from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "amount",
            "transaction_type",
            "description",
            "balance_after_transaction",
            "created_at",
        ]
        read_only_fields = ["id", "balance_after_transaction", "created_at"]
