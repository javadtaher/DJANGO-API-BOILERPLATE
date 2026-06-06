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
        allow_null=True,
        required=False,
        error_messages={
            'invalid': 'Invalid username.'
        }
    )

    email = serializers.CharField(
        allow_null=True,
        required=False,
        error_messages={
            'invalid': 'Invalid email.'
        }
    )

    phone = serializers.CharField(
        allow_null=True,
        required=False,
        error_messages={
            'invalid': 'Invalid email.'
        }
    )

    password = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Please provide your password.',
            'invalid': 'Invalid password.',
        }
    )

    default_error_messages = {
        'invalid_credentials': 'Username, email, phone or password is wrong',
        'no_identifier': 'Please provide at least one of username, email, or phone'
    }

    class Meta:
        model = Users
        fields = ['username', 'email', 'phone', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        phone = attrs.get('phone')
        password = attrs.get('password')

        if not any([username, email, phone]):
            self.fail('no_identifier')

        from django.contrib.auth import authenticate
        user = None
        if username:
            user = authenticate(username=username, password=password)
        if not user and email:
            try:
                user_obj = Users.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
            except Users.DoesNotExist:
                pass
        if not user and phone:
            try:
                user_obj = Users.objects.get(phone=phone)
                user = authenticate(username=user_obj.username, password=password)
            except Users.DoesNotExist:
                pass
        if not user:
            self.fail('invalid_credentials')
        attrs['user'] = user
        return attrs


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

    default_error_messages = {
        'no_identifier': 'Please provide email or username',
        'user_not_found': 'please enter valid email or username !!!'
    }

    class Meta:
        model = Users
        fields = ['email', 'username']

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        if not any([email, username]):
            self.fail('no_identifier')

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
            self.fail('user_not_found')

        attrs['user'] = user
        return attrs


class UserEditPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Required field: code is required',
        }
    )
    new_password = serializers.CharField(
        required=True,
        min_length=8,
        error_messages={
            'required': 'Required field: new password is required',
            'min_length': 'Short password'
        }
    )
    confirm_password = serializers.CharField(
        required=True,
        min_length=8,
        error_messages={
            'required': 'Required field: confirm password is required',
            'min_length': 'Short password',
            'password_mismatch': 'new password and confirm password are not the same'
        }
    )

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(self.fields['confirm_password'].error_messages['password_mismatch'], code='password_mismatch')
        return data

    class Meta:
        model = Users
        fields = ['old_password', 'new_password', 'confirm_password']


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        error_messages={
            'required': 'Please provide your email.',
            'blank': 'Email should not be blank.',
            'unique': 'This email is already taken'
        }
    )
    username = serializers.CharField(
        max_length=100,
        error_messages={
            'required': 'Please provide your username.',
            'blank': 'Username should not be blank.',
            'unique': 'This username is not available',
            'max_length': 'message length is larger'
        }
    )
    phone = serializers.CharField(
        max_length=15,
        error_messages={
            'required': 'Please provide your phone number.',
            'blank': 'Phone should not be blank.',
            'unique': 'This phone number is already registered',
            'max_length': 'Phone number is too long'
        }
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            'required': 'Please provide your password.',
            'blank': 'Password should not be blank.',
            'min_length': 'Short password'
        }
    )

    class Meta:
        model = Users
        fields = ['email', 'username', 'phone', 'password']

    def validate_email(self, value):
        if Users.objects.filter(email=value).exists():
            raise serializers.ValidationError(self.fields['email'].error_messages['unique'], code='unique')
        return value

    def validate_username(self, value):
        if Users.objects.filter(username=value).exists():
            raise serializers.ValidationError(self.fields['username'].error_messages['unique'], code='unique')
        return value

    def validate_phone(self, value):
        if Users.objects.filter(phone=value).exists():
            raise serializers.ValidationError(self.fields['phone'].error_messages['unique'], code='unique')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Users.objects.create_user(**validated_data, password=password)
        return user


class ResLoginSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=1000)
    refresh_token = serializers.CharField()
    is_new_user = serializers.BooleanField()
