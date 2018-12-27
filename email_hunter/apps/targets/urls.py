from django.urls import path, include
from . import views

urlpatterns = [
    path('targets/', views.TargetListView.as_view(), name='target_list_view'),
    path('targets/<pk>', views.TargetUpdateView.as_view(), name='target_update_view'),
    path('targets/upload', views.TargetUploadView.as_view(), name='target_upload_view'),
    path('files/', views.FileListView.as_view(), name='target_file_list_view'),
    path('files/<pk>/edit', views.FileUpdateView.as_view(), name='target_file_update_view'),
]