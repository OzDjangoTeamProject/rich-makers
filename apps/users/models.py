from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)

    # membership_status: FREE, PREMIUM 관리
    membership_status = models.CharField(max_length=10, default="FREE")

    def __str__(self):
        return self.username  # 로그인할 때 사용하는 아이디 표시
