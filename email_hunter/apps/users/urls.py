from django.urls import path, include
from . import views


app_name = 'email_hunter.apps.users'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard_view'),
]