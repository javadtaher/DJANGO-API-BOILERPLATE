from django.urls import path

from django_design_pattern_app.api.v1.admin.users import ManageSupportView, ManageEditorView

admins_url = [
    path('editor/manage/', ManageEditorView.as_view(), name='S_register'),
    path('support/manage/', ManageSupportView.as_view(), name='E_register'),
]
