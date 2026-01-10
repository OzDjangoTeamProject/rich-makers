from rest_framework import serializers

# ==========================================
# 1. Users App (회원 관리)
# ==========================================

# 회원가입 (POST /api/users/signup/)
class UserSignupRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    nickname = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False)

class UserSignupResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    nickname = serializers.CharField()
    membership_status = serializers.CharField()

"""
POST /api/users/signup/
Request Body: UserSignupRequestSerializer
Response Body: UserSignupResponseSerializer
Status Code: 201 Created
"""

# 유저 프로필 (GET/PATCH /api/users/profile/)
class UserProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(read_only=True)
    nickname = serializers.CharField()
    phone_number = serializers.CharField()
    membership_status = serializers.CharField(read_only=True)

"""
GET /api/users/profile/
Response Body: UserProfileSerializer
Status Code: 200 OK

PATCH /api/users/profile/
Request Body: UserProfileSerializer (Partial)
Response Body: UserProfileSerializer
Status Code: 200 OK
"""

# ==========================================
# 2. Accounts App (계좌 관리)
# ==========================================

# 계좌 생성 및 목록 (POST & GET /api/accounts/)
class AccountRequestSerializer(serializers.Serializer):
    account_number = serializers.CharField()
    bank_code = serializers.CharField() # KB, Shinhan 등
    account_type = serializers.CharField() # Saving, Minus 등
    balance = serializers.IntegerField(default=0)

class AccountResponseSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    account_number = serializers.CharField()
    bank_code = serializers.CharField()
    balance = serializers.IntegerField()

"""
POST /api/accounts/
Request Body: AccountRequestSerializer
Response Body: AccountResponseSerializer
Status Code: 201 Created

GET /api/accounts/
Response Body: AccountResponseSerializer(many=True)
Status Code: 200 OK
"""

# ==========================================
# 3. Transactions App (거래 내역)
# ==========================================

# 거래 내역 기록 (POST /api/transactions/)
class TransactionCreateRequestSerializer(serializers.Serializer):
    account_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    tx_type = serializers.ChoiceField(choices=['INCOME', 'EXPENSE'])
    tx_detail = serializers.CharField()
    payment_method = serializers.ChoiceField(choices=['CASH', 'CARD', 'TRANSFER'])

class TransactionResponseSerializer(serializers.Serializer):
    tx_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    balance_after_tx = serializers.IntegerField()
    tx_type = serializers.CharField()
    created_at = serializers.DateTimeField()

"""
POST /api/transactions/
Request Body: TransactionCreateRequestSerializer
Response Body: TransactionResponseSerializer
Status Code: 201 Created
"""

# ==========================================
# 4. Notifications App (알림)
# ==========================================

# 알림 읽음 처리 (PATCH /api/notifications/<int:pk>/read/)
class NotificationReadResponseSerializer(serializers.Serializer):
    noti_id = serializers.IntegerField()
    is_read = serializers.BooleanField()
    message = serializers.CharField()

"""
PATCH /api/notifications/<int:pk>/read/
Request Body: None (Logic in View)
Response Body: NotificationReadResponseSerializer
Status Code: 200 OK
"""