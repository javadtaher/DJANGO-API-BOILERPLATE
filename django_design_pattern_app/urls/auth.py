from django.urls import path

from django_design_pattern_app.api.v1.auth.auth import RegisterView, LoginView

auth_url = [

    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login')

]

