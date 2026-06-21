from django.urls import path, include
from django_design_pattern_app.urls.admin.admin import admin_url
from .products import products_url
from .users import user_url
from .auth import auth_url
from .admins import admins_url


urlpatterns = [
    path('', include(auth_url)),
    path('', include(user_url)),
    path('', include(admin_url)),
    path('', include(admins_url)),
    path('', include(products_url)),
    path('', include('django_prometheus.urls')),
]
