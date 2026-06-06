import os

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from django_design_pattern_app.injector.base_injector import BaseInjector
from django_design_pattern_app.middleware.exceptions import handle_exceptions
from django_design_pattern_app.middleware.validate import validate_serializer
from django_design_pattern_app.models import Users
from django_design_pattern_app.repositories.users_repo import UsersRepo
from django_design_pattern_app.middleware.response import APIResponse
from django_design_pattern_app.permissions import permissions
from django_design_pattern_app.permissions.permissions import IsSuperUser
from django_design_pattern_app.serializers.users.users_serializers import UserInfoUpdateSerializer, \
    UserGetAvatarSerializer


class BaseView(APIView, AutoSchema):
    user_repo = BaseInjector.get(UsersRepo)


class IndexView(BaseView, generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, IsSuperUser)
    serializer_class = UserInfoUpdateSerializer

    @validate_serializer()
    @handle_exceptions
    def get(self, request):
        """
        This is a test view, which is used to test the health of other services.
        It calls the database, minio, and elasticsearch.
        """
        self.user_repo.get_user_by_id(request.user.id)
        return APIResponse(data=True)


class AvatarUploadView(BaseView, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserGetAvatarSerializer

    @handle_exceptions
    def post(self, request):
        file = request.FILES.get('avatar')
        if not file:
            return APIResponse(data="no file uploaded", error_code=1, status=400)

        ext = file.name.split('.')[-1].lower()
        allowed = {'jpg', 'jpeg', 'png'}
        if ext not in allowed:
            return APIResponse(data="only jpg, jpeg, png, gif, webp allowed", error_code=1, status=400)

        max_size = 2 * 1024 * 1024
        if file.size > max_size:
            return APIResponse(data="file size must be less than 2MB", error_code=1, status=400)

        bucket = os.getenv("BUCKET_NAME")

        self.user_repo.service_minio.create_bucket(bucket)

        object_name = f"users/{request.user.username}/{file.name}"
        self.user_repo.service_minio.upload_file(bucket, object_name, file.read())

        request.user.avatar = object_name
        request.user.save(update_fields=['avatar'])

        return APIResponse(data={
            "avatar_url": f"/api/v1/avatar/{request.user.username}"
        }, success_code=2000)


class AvatarDownloadView(BaseView, generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserInfoUpdateSerializer

    @handle_exceptions
    def get(self, request, username):
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return APIResponse(data="user not found", error_code=1, status=404)

        if not user.avatar:
            return APIResponse(data="no avatar", error_code=1, status=404)

        minio_sdk = self.user_repo.service_minio
        bucket = os.getenv("BUCKET_NAME")
        file_bytes = minio_sdk.get_object_contents(bucket, user.avatar)

        from django.http import HttpResponse
        ext = user.avatar.split('.')[-1] if '.' in user.avatar else 'jpg'
        return HttpResponse(file_bytes, content_type=f"image/{ext}")


class AvatarDeleteView(BaseView, generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserGetAvatarSerializer

    @handle_exceptions
    def delete(self, request):
        user = request.user
        filename = request.GET.get('filename')

        minio_sdk = self.user_repo.service_minio
        bucket = os.getenv("BUCKET_NAME")
        prefix = f"users/{user.username}/"

        if filename:
            object_name = f"{prefix}{filename}"
            minio_sdk.delete_object(bucket, object_name)
        else:
            if not user.avatar:
                return APIResponse(data="no avatar", error_code=1, status=404)
            minio_sdk.delete_object(bucket, user.avatar)

        remaining = minio_sdk.search_objects(bucket, prefix=prefix, recursive=True)

        latest = None
        for obj in remaining:
            if latest is None or obj.last_modified > latest.last_modified:
                latest = obj

        if latest:
            user.avatar = latest.object_name
        else:
            user.avatar = None

        user.save(update_fields=['avatar'])

        return APIResponse(data="avatar deleted", success_code=2000)
