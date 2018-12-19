from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.TargetListView.as_view(), name='target_list_view'),
    path('upload', views.TargetUploadView.as_view(), name='target_upload_view'),
]