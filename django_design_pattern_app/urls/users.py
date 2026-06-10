from django.urls import path

from django_design_pattern_app.api.v1.users.users import (
    IndexView, AvatarUploadView, AvatarDownloadView, AvatarDeleteView
)


user_url = [
    path('index', IndexView.as_view(), name='index'),
    path('update', IndexView.as_view(), name='update'),
    path('avatar/upload/', AvatarUploadView.as_view(), name='avatar-upload'),
    path('avatar/delete/', AvatarDeleteView.as_view(), name='avatar-delete'),
    path('avatar/<str:username>/', AvatarDownloadView.as_view(), name='avatar-download'),
]
