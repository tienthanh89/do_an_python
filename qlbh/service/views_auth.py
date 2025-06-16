from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
import re

USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9\-_@]{1,20}$')

@api_view(['POST'])
def register_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    confirm_password = request.data.get("confirm_password")

    if not username:
        return Response({"error": "❌ Username không được để trống."}, status=status.HTTP_400_BAD_REQUEST)
    if not USERNAME_PATTERN.fullmatch(username):
        return Response({"error": "❌ Username không hợp lệ."}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({"error": "❌ Username đã tồn tại."}, status=status.HTTP_400_BAD_REQUEST)
    if not password or len(password) < 3:
        return Response({"error": "❌ Password quá ngắn."}, status=status.HTTP_400_BAD_REQUEST)
    if password != confirm_password:
        return Response({"error": "❌ Confirm password không trùng khớp."}, status=status.HTTP_400_BAD_REQUEST)

    User.objects.create_user(username=username, password=password)
    return Response({"message": "✅ Đăng ký thành công!"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        return Response({"message": "✅ Đăng nhập thành công!"}, status=status.HTTP_200_OK)
    return Response({"error": "❌ Sai username hoặc password."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def forgot_password_view(request):
    username = request.data.get("username")
    new_password = request.data.get("new_password")
    confirm_new_password = request.data.get("confirm_new_password")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "❌ Username không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

    if not new_password or len(new_password) < 3:
        return Response({"error": "❌ Mật khẩu mới quá ngắn."}, status=status.HTTP_400_BAD_REQUEST)
    if new_password != confirm_new_password:
        return Response({"error": "❌ Confirm password không trùng khớp."}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({"message": "✅ Đặt lại mật khẩu thành công!"}, status=status.HTTP_200_OK)
