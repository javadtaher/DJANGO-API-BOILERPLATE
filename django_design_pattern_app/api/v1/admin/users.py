from rest_framework import generics

from django_design_pattern_app.middleware.exceptions import handle_exceptions
from django_design_pattern_app.middleware.response import APIResponse
from django_design_pattern_app.middleware.validate import validate_serializer
from django_design_pattern_app.permissions import permissions
from django_design_pattern_app.api.v1.users.users import BaseView
from django_design_pattern_app.serializers.admin.user_serializers import ManageAdminsSerializer
from django_design_pattern_app.services.email.tasks import send_email_task


class ManageEditorView(BaseView, generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminOrEditor, )
    serializer_class = ManageAdminsSerializer

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.rule_id = serializer.validated_data['rule_id']
        if user.rule_id == 0:
            user.state = 'User'
        elif user.rule_id == 2:
            user.state = 'Super Editor'
        elif user.rule_id == 3:
            user.state = 'Support'
        user.save()

        content = f"<p><h3>Your state is changed successfully</h3><h3>You are {user.state} now</h3></p>"
        if not user.is_superuser:
            send_email_task.delay(to=user.email, subject="Change state", body=content)
        return APIResponse(data={
            "user": user.username,
            "state": user.state,
        }, success_code=2000)


class ManageSupportView(BaseView, generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.CanManageSupport)
    serializer_class = ManageAdminsSerializer

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.rule_id = serializer.validated_data['rule_id']
        if user.rule_id == 0:
            user.state = 'User'
        elif user.rule_id == 3:
            user.state = 'Support'
        user.save()

        content = f"<p><h3>Your state is changed successfully</h3><h3>You are {user.state} now</h3></p>"
        if not user.is_superuser:
            send_email_task.delay(to=user.email, subject="Change state", body=content)
        return APIResponse(data={
            "user": user.username,
            "state": user.state,
        }, success_code=2000)
