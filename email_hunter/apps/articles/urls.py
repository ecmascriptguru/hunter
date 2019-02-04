from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list_view'),
    path('upload', views.ArticleUploadView.as_view(), name='article_upload_view'),
]