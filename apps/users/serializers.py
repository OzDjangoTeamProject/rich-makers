# 장고 및 DRF 도구 가져오기
from django.contrib.auth.hashers import make_password  # 비밀번호 암호화 도구
from rest_framework import serializers

from .models import User

"""
ModelSerializer
장고 모델과 1:1로 매칭되는 시리얼라이저
필드 이름만 적어주면 장고가 알아서 검증 로직을 만듦

make_password
비밀번호 암호화 도구
데이터베이스 해킹당해도 비밀번호를 알 수 없도록 해싱(Hashing) 처리
"""


class UserSignupSerializer(serializers.ModelSerializer):
    """
    회원가입을 위한 시리얼라이저
    사용자로부터 받은 데이터를 검증하고 DB에 저장
    """

    # 비밀번호는 쓰기 전용으로 설정
    # 응답 데이터에 포함되지 않도록 보호
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password", "nickname", "phone_number"]

    def validate_password(self, value):
        """
        비밀번호를 DB에 그대로 저장 X
        암호화 과정 필요
        """
        return make_password(value)  # 👈암호화!

    def create(self, validated_data):
        """
        실제로 유저 객체를 생성하는 부분
        """
        return User.objects.create(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    유저 정보 확인 및 수정을 위한 시리얼라이저
    """

    class Meta:
        model = User

        # 확인 및 수정하고 싶은 필드들만 나열
        fields = ["id", "username", "email", "nickname", "phone_number", "membership_status"]

        # username은 중복 문제와 고유성 때문에 수정을 못 하게 read_only로 설정하는 것이 시니어의 팁!
        read_only_fields = ["id", "username", "membership_status"]
