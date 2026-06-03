import random

from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from django_design_pattern_app.api.v1.users.users import BaseView
from django_design_pattern_app.email.sendemail import Send_Email
from django_design_pattern_app.middleware.exceptions import handle_exceptions
from django_design_pattern_app.middleware.response import APIResponse
from django_design_pattern_app.middleware.validate import validate_serializer
from django_design_pattern_app.models import Users
from django_design_pattern_app.permissions import permissions
from django_design_pattern_app.serializers.users.users_serializers import UserRegisterSerializer, \
    UserInfoUpdateSerializer, \
    UserLoginSerializer, UserForgetPasswordSerializer, UserEditPasswordSerializer


class UserRegisterView(BaseView, generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        content = f"<p><h3>your account created successfully<h3><p>"
        Send_Email(to=user.email, subject="registration", body=content)
        return APIResponse(data={
            "user": user.username,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, success_code=2000, status=status.HTTP_201_CREATED)


class UserLoginView(BaseView, generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return APIResponse(data={
                "user": user.username,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, success_code=2000)
        return APIResponse(data={
            'message': 'username or password is wrong'
        }, error_code=1, status=401)


class EditUserView(BaseView, generics.GenericAPIView):
    serializer_class = UserInfoUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        serializer = self.get_serializer(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return APIResponse(data=True)


class UserForgetPassView(BaseView, generics.GenericAPIView):
    serializer_class = UserForgetPasswordSerializer
    permission_classes = [AllowAny]

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')

        user = None
        if email:
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                pass
        elif username:
            try:
                user = Users.objects.get(username=username)
            except Users.DoesNotExist:
                pass

        if not user:
            return APIResponse(data="please enter valid email or username !!!", error_code=1000, status=401)

        new_password = f"{random.randint(0, 999999):06d}"
        user.set_password(new_password)
        user.save()

        Send_Email(to=user.email, subject="password reset", body=f"your new password: {new_password}")

        return APIResponse(data={
            'message': 'new password sent to your email'
        }, success_code=2000)


class UserEditPassView(BaseView, generics.GenericAPIView):
    serializer_class = UserEditPasswordSerializer
    permission_classes = [AllowAny]

    @validate_serializer()
    @handle_exceptions
    def post(self, request, username=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return APIResponse(data="user not found", error_code=1000, status=404)

        if not user.check_password(serializer.validated_data['old_password']):
            return APIResponse(data="old password is incorrect", error_code=1000, status=401)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        Send_Email(to=user.email, subject="change password", body="your password has been changed")

        access_str = request.headers.get('Authorization', '').replace('Bearer ', '')
        if access_str:
            access = AccessToken(access_str)
            cache.set(f'blacklist_access_{access["jti"]}', True, timeout=300)

        refresh_str = request.data.get('refresh')
        if refresh_str:
            refresh = RefreshToken(refresh_str)
            refresh.blacklist()

        return APIResponse(data={
            'user': user.username,
            'message': 'your password has been changed'
        }, success_code=2000)
