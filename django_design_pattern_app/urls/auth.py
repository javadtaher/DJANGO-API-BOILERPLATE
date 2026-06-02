from django.urls import path

from django_design_pattern_app.api.v1.auth.auth import UserRegisterView, UserForgetPassView, UserLoginView, \
    UserEditPassView

auth_url = [

    path('register', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('login/forgetpass', UserForgetPassView.as_view(), name='forget'),
    path('login/editpass', UserEditPassView.as_view(), name='editpass'),
]
