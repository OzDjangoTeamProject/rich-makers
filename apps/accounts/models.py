from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("이메일은 필수로 입력해주세요.")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # 이메일 인증여부
    is_email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class EmailVerificationRequired(models.Model):
        user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="email_verification"
        )
        token = models.UUIDField(default=uuid.uuid4, unique=True)
        created_at = models.DateTimeField(auto_now_add=True)