from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CredentialListView.as_view(), name='credential_list_view'),
]