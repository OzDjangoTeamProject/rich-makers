from rest_framework import serializers

# ==========================================
# 1. Users App (회원 관리)
# ==========================================


# 회원가입 [3단계 미션2]
class UserSignupRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, help_text="사용자 식별 아이디")
    email = serializers.EmailField(help_text="비밀번호 찾기 등에 사용될 이메일 주소")
    password = serializers.CharField(write_only=True, min_length=8, help_text="8자 이상의 영문/숫자 조합")
    nickname = serializers.CharField(required=False, help_text="서비스 내에서 보일 이름")


# 로그인 [3단계 미션3]
class UserLoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="가입 시 등록한 아이디")
    password = serializers.CharField(write_only=True, help_text="비밀번호")


# 유저 프로필 [3단계 미션5]
class UserProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(read_only=True, help_text="이메일 (수정 불가)")
    nickname = serializers.CharField(help_text="수정할 닉네임")
    phone_number = serializers.CharField(help_text="010-0000-0000 형식의 연락처")


# ==========================================
# 2. Accounts App (계좌 관리)
# ==========================================


# 계좌 목록 및 생성 [4단계 미션1, 2]
class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    account_number = serializers.CharField(help_text="하이픈(-)을 포함한 계좌번호")
    bank_code = serializers.CharField(help_text="은행 코드 (예: 088-신한, 004-국민 등)")
    balance = serializers.DecimalField(max_digits=20, decimal_places=2, help_text="현재 계좌 잔액")


# ==========================================
# 3. Transactions App (거래 내역)
# ==========================================


# 거래 내역 기록/목록 [4단계 미션4]
class TransactionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    account = serializers.IntegerField(help_text="거래가 발생한 계좌의 ID")
    amount = serializers.DecimalField(max_digits=20, decimal_places=2, help_text="거래 금액")
    tx_type = serializers.ChoiceField(choices=["DEPOSIT", "WITHDRAW"], help_text="입금(DEPOSIT) 또는 출금(WITHDRAW)")
    tx_detail = serializers.CharField(help_text="거래 상세 내용 (예: 스타벅스)")
    created_at = serializers.DateTimeField(read_only=True, help_text="거래 일시")


# ==========================================
# 4. Analysis App (분석)
# ==========================================


# 분석 결과 조회 및 생성 [5단계]
class AnalysisSerializer(serializers.Serializer):
    target_type = serializers.CharField(help_text="분석 대상 (총 지출/총 수입)")
    period_unit = serializers.CharField(help_text="분석 주기 (일간/주간/월간/연간)")
    total_amount = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True, help_text="분석 결과 총액")


# ==========================================
# 5. Notifications App (알림)
# ==========================================


# 알림 목록 조회 [6단계]
class NotificationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    message = serializers.CharField(help_text="알림 내용")
    is_read = serializers.BooleanField(help_text="읽음 여부")
