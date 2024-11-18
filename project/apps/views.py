from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import Diary
from .serializers import DiarySerializer, UserRegistrationSerializer, UserLoginSerializer


# 회원가입 API
class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


# 로그인 API
class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 일기 등록 API
class DiaryCreateAPIView(generics.CreateAPIView):
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    # 사용자 정보 포함하여 일기 생성
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 특정 사용자의 모든 일기 목록 조회 API
class DiaryListAPIView(generics.ListAPIView):
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    # 현재 로그인한 사용자의 일기만 조회
    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)


# 일기 수정 API
class DiaryUpdateAPIView(generics.UpdateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    # 현재 사용자 소유의 일기만 수정 가능하도록 필터링
    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)


# 일기 삭제 API
class DiaryDeleteAPIView(generics.DestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    permission_classes = [permissions.IsAuthenticated]

    # 현재 사용자 소유의 일기만 삭제 가능하도록 필터링
    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)
