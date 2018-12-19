from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CredentialListView.as_view(), name='credential_list_view'),
    path('/upload', views.CredentialUploadView.as_view(), name='credential_upload_view'),
    path('/new', views.CredentialCreateView.as_view(), name='credential_create_view'),
]