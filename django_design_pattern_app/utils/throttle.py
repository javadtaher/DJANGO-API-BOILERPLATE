import time

from django.core.cache import cache as default_cache
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from django_design_pattern_app.services.email.tasks import send_email_task

from django_design_pattern_app.services.email.tasks import send_email_task

COOLDOWN_KEY = "throttle_cooldown_{scope}_{ident}"
COOLDOWN_DURATION = 600


class CooldownAnonRateThrottle(AnonRateThrottle):
    def allow_request(self, request, view):
        self._ident = self.get_ident(request)
        cooldown_key = COOLDOWN_KEY.format(scope=self.scope, ident=self._ident)

        if default_cache.get(cooldown_key):
            return False

        allowed = super().allow_request(request, view)
        if not allowed:
            default_cache.set(cooldown_key, 1, COOLDOWN_DURATION)
            self.cache.delete(self.key)
            return False

        return True

    def wait(self):
        key = COOLDOWN_KEY.format(scope=self.scope, ident=self._ident)
        remaining = default_cache.ttl(key)
        return remaining if remaining and remaining > 0 else 0


class CooldownUserRateThrottle(UserRateThrottle):
    def allow_request(self, request, view):
        if request.user.is_authenticated:
            self._ident = request.user.pk
        else:
            self._ident = self.get_ident(request)
        cooldown_key = COOLDOWN_KEY.format(scope=self.scope, ident=self._ident)

        if default_cache.get(cooldown_key):
            if request.user.is_authenticated:
                send_email_task.delay(
                    to=request.user.email,
                    subject="System error",
                    body=f"You have sent too many requests permanently. You can try again in {int(self.wait()/60)} : {int(self.wait())-int(self.wait()/60)*60} min"
                )
            return False

        allowed = super().allow_request(request, view)
        if not allowed:
            default_cache.set(cooldown_key, 1, COOLDOWN_DURATION)
            self.cache.delete(self.key)
            if request.user.is_authenticated:
                send_email_task.delay(
                    to=request.user.email,
                    subject="System error",
                    body=f"You have sent too many requests permanently. You can try again in {int(self.wait()/60)} : {int(self.wait())-int(self.wait()/60)*60} min"
                )
            return False

        return True

    def wait(self):
        key = COOLDOWN_KEY.format(scope=self.scope, ident=self._ident)
        remaining = default_cache.ttl(key)
        return remaining if remaining and remaining > 0 else 0