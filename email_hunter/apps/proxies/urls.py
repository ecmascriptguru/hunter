from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ProxyListView.as_view(), name='proxy_list_view'),
]