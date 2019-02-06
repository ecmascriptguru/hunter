from django.urls import path, include
from . import views

urlpatterns = [
    path('buckets/', views.BucketListView.as_view(), name='bucket_list_view'),
    path('buckets/<int:pk>', views.BucketUpdateView.as_view(), name='bucket_update_view'),
    path('articles/', views.ArticleListView.as_view(), name='article_list_view'),
    path('articles/upload', views.ArticleUploadView.as_view(), name='article_upload_view'),
]