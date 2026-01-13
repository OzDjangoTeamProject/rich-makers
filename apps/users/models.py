from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from apps.constants import MEMBERSHIP_CHOICES


class User(AbstractUser):
    """
    서비스의 사용자 모델
    - 기본 제공 필드
    - 이메일 필드: 이메일 기반 로그인
    - 휴대폰 검증 기능
    """

    email = models.EmailField(unique=True)  # 중복 가입 방지

    # 전화번호 유효성 검사 (010-0000-0000 형식)
    phone_regex = RegexValidator(
        regex=r"^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$", message="전화번호 형식이 올바르지 않습니다."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=20)

    # membership_status: FREE, PREMIUM 관리
    membership_status = models.CharField(
        max_length=10,
        choices=MEMBERSHIP_CHOICES,
        default="FREE",
        verbose_name="멤버십 상태",
    )

    def __str__(self):
        return self.username  # 로그인할 때 사용하는 아이디 표시
