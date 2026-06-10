from rest_framework import serializers

from django_design_pattern_app.models import Users
from django_design_pattern_app.permissions.permissions import CanManageEditor, CanManageSupport


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        allow_null=True,
        required=False,
        error_messages={
            'null': 'Username cannot be null.',
            'invalid': 'Invalid username.'
        }
    )

    password = serializers.CharField(
        allow_null=True,
        required=False,
        error_messages={
            'null': 'Password cannot be null.',
            'invalid': 'Invalid password.',
        }
    )


class StatusDeviceSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        allow_null=True,
        required=False,
        error_messages={
            'null': 'Username cannot be null.',
            'invalid': 'Invalid username.'
        }
    )
    is_active = serializers.BooleanField(
        required=False
    )


class DeleteDeviceSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        allow_null=True,
        required=False,
        error_messages={
            'null': 'Username cannot be null.',
            'invalid': 'Invalid username.'
        }
    )


class ManageAdminsSerializer(serializers.Serializer):
    rule_id = serializers.IntegerField(
        min_value=0,
        max_value=3,
        required=True,
        error_messages={
            'null': 'Rule id cannot be null',
            'min_value': 'Invalid rule id',
            'max_value': 'Invalid rule id',
            'required': 'Rule id is required',
            'invalid': 'Rule id is invalid',
        }
    )
    username = serializers.CharField(
        max_length=100,
        required=False,
        error_messages={
            'null': 'Username id cannot be null',
            'max_length': 'Username is too long',
        }
    )
    email = serializers.EmailField(
        required=False,
        error_messages={
            'null': 'Email cannot be null',
        }
    )
    phone = serializers.CharField(
        required=False,
        min_length=11,
        max_length=15,
        error_messages={
            'null': 'Phone number cannot be null',
            'max_length': 'Phone number is too long',
            'min_length': 'Phone number is too short',
        }
    )

    default_error_messages = {
        'invalid_credentials': 'Username, email, phone or password is wrong',
        'no_identifier': 'Please provide at least one of username, email, or phone',
        'no_permission': 'You are not authorized to do this',
    }

    def validate(self, attrs):
        rule_id = attrs.get('rule_id')
        username = attrs.get('username')
        email = attrs.get('email')
        phone = attrs.get('phone')

        if not any([username, email, phone]):
            self.fail('no_identifier')
        if rule_id == 1:
            self.fail('invalid')
        user = None
        if username:
            user = Users.objects.get(username=username)
        if not user and email:
            try:
                user = Users.objects.get(email=email)
            except Users.DoesNotExist:
                pass
        if not user and phone:
            try:
                user = Users.objects.get(phone=phone)
            except Users.DoesNotExist:
                pass
        if not user:
            self.fail('invalid_credentials')
        attrs['user'] = user
        return attrs

    def validate_rule_id(self, value):
        request = self.context['request']
        if value == 2:
            if not CanManageEditor().has_permission(request, self):
                self.fail('no_permission')
        elif value == 3:
            if not CanManageSupport().has_permission(request, self):
                self.fail('no_permission')
        return value

    class Meta:
        model = Users
        fields = ['rule_id', 'username', 'email', 'phone']
