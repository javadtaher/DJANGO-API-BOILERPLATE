from django_design_pattern_app.monitoring.metrics import user_count
from django_design_pattern_app.models.users import Users


class UpdateUserCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_count.set(Users.objects.count())
        response = self.get_response(request)
        return response
