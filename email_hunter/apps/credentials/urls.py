from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CredentialListView.as_view(), name='credential_list_view'),
    path('upload', views.CredentialUploadView.as_view(), name='credential_upload_view'),
    path('new', views.CredentialCreateView.as_view(), name='credential_create_view'),
    path('<pk>', views.CredentialUpdateView.as_view(), name='credential_update_view'),
    path('<pk>/delete', views.CredentialDeleteView.as_view(), name='credential_delete_view'),
]