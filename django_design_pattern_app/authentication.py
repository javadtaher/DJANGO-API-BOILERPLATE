from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.core.cache import cache


class BlacklistJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result:
            user, validated_token = result
            jti = validated_token.get('jti')
            if cache.get(f'blacklist_access_{jti}'):
                raise InvalidToken("Token is blacklisted")
        return result
