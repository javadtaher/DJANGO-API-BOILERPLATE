from prometheus_client import Gauge
from django.apps import apps

user_count = Gauge('app_users_total', 'Total number of registered users')


def update_user_count():
    Users = apps.get_model('django_design_pattern_app', 'Users')
    user_count.set(Users.objects.count())
