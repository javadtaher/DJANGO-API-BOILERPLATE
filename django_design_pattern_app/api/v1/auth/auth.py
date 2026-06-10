import random

from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from django_design_pattern_app.api.v1.users.users import BaseView
from django_design_pattern_app.services.email.tasks import send_email_task
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
        content = f"<p><h3>your account created successfully</h3></p>"
        if not user.is_superuser:
            send_email_task.delay(to=user.email, subject="registration", body=content)
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
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        if not user.is_superuser:
            send_email_task.delay(to=user.email, subject="NEW LOGIN", body="new login to your account")
        return APIResponse(data={
            "user": user.username,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, success_code=2000)


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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        new_password = f"{random.randint(0, 999999):06d}"
        user.set_password(new_password)
        user.save()
        if not user.is_superuser:
            send_email_task.delay(to=user.email, subject="password reset", body=f"your code: {new_password}")
        else:
            print(f"new password: {new_password}")

        return APIResponse(data={
            'message': 'code sent to your email'
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
            return APIResponse(data="Code is incorrect", error_code=1000, status=401)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        if not user.is_superuser:
            send_email_task.delay(to=user.email, subject="change password", body="your password has been changed")

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
