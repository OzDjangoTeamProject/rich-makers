from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    # membership_status: FREE, PREMIUM 관리
    membership_status = models.CharField(max_length=10, default="FREE")

    # 아래 두 필드를 추가해야 Django 기본 모델과 충돌하지 않습니다.
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # 별명 설정
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # 별명 설정
        blank=True,
    )

    def __str__(self):
        return self.username