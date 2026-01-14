from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    계좌 등록 및 조회를 위한 시리얼라이저
    """

    transaction_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Account
        fields = ["id", "account_name", "account_number", "balance", "transaction_count", "created_at"]
        read_only_fields = ["id", "account_number", "balance", "created_at"]

    def create(self, validated_data):
        # 계좌 번호를 자동으로 생성하여 저장합니다.
        validated_data["account_number"] = Account.generate_account_number()
        # 현재 로그인한 유저를 주인으로 설정합니다.
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
