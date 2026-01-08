from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from serializers import RegistrationSerializer

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "회원가입 성공 이메일 인증을 해주세요"},
            status=status.HTTP_201_CREATED
        )