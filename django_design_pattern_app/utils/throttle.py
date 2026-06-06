from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class CustomAnonRateThrottle(AnonRateThrottle):
    def wait_message(self):
        return 'تعداد درخواست ها زیاد بوده لطفا بعدا امتحان کنین'


class CustomUserRateThrottle(UserRateThrottle):
    def wait_message(self):
        return 'تعداد درخواست ها زیاد بوده لطفا بعدا امتحان کنین'
