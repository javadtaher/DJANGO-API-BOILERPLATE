from rest_framework import serializers
from django_design_pattern_app.models.users import Users


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        allow_blank=True,
        required=False,
        max_length=100,
        error_messages={
            'max_length': 'message length is larger'
        }
    )

    first_name = serializers.CharField(
        allow_blank=True,
        required=False,
        max_length=100,
        error_messages={
            'max_length': 'message length is larger'
        }
    )

    last_name = serializers.CharField(
        allow_blank=True,
        required=False,
        max_length=100,
        error_messages={
            'max_length': 'message length is larger'
        }
    )

    job = serializers.CharField(
        allow_blank=True,
        required=False,
        max_length=100,
        error_messages={
            'max_length': 'message length is larger'
        }
    )

    state = serializers.CharField(
        allow_blank=True,
        required=False,
        max_length=100,
        error_messages={
            'max_length': 'message length is larger'
        }
    )

    city = serializers.CharField(
        allow_blank=True,
        required=False,
        max_length=100,
        error_messages={
            'max_length': 'message length is larger'
        }
    )

    avatar = serializers.CharField(
        allow_blank=True,
        required=False,
        max_length=500,
    )

    class Meta:
        model = Users
        fields = ['email', 'first_name', 'last_name', 'job', 'state', 'avatar', 'city']


class UserGetAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.CharField(
        allow_blank=True,
        required=False,
        max_length=500,
    )

    class Meta:
        model = Users
        fields = ['avatar']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        # allow_null=True,
        required=True,
        error_messages={
            'required': 'Please provide your city.',
            'invalid': 'Invalid username.'
        }
    )

    password = serializers.CharField(
        # allow_null=True,
        required=True,
        error_messages={
            'required': 'Please provide your city.',
            'invalid': 'Invalid password.',
        }
    )

    class Meta:
        model = Users
        fields = ['username', 'password']


class UserForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        allow_null=True,
        required=False,
        error_messages={
            'invalid': 'Invalid email.'
        }
    )

    username = serializers.CharField(
        allow_null=True,
        required=False,
        error_messages={
            'invalid': 'Invalid username.'
        }
    )

    class Meta:
        model = Users
        fields = ['email', 'username']


class UserEditPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Required field',
        }
    )
    new_password = serializers.CharField(
        required=True,
        min_length=8,
        error_messages={
            'required': 'Required field',
            'min_length': 'Short password'
        }
    )
    confirm_password = serializers.CharField(
        required=True,
        min_length=8,
        error_messages={
            'required': 'Required field',
            'min_length': 'Short password'
        }
    )

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("passwords do not match", code="password_mismatch")
        return data

    class Meta:
        model = Users
        fields = ['old_password', 'new_password', 'confirm_password']


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        error_messages={
            'required': 'Please provide your email.',
            'blank': 'Email should not be blank.',
        }
    )
    username = serializers.CharField(
        max_length=100,
        error_messages={
            'unique': 'This username is not available',
            'required': 'Please provide your username.',
            'blank': 'Username should not be blank.',
            'max_length': 'message length is larger'
        }
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            'required': 'Please provide your city.',
            'blank': 'City should not be blank.',
            'min_length': 'Short password'
        }
    )

    class Meta:
        model = Users
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Users.objects.create_user(**validated_data, password=password)
        return user


class ResLoginSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=1000)
    refresh_token = serializers.CharField()
    is_new_user = serializers.BooleanField()
