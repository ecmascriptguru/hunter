from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.LeadListView.as_view(), name='lead_list_view'),
]