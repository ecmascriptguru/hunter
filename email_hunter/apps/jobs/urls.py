from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list_view'),
    path('<pk>', views.JobDetailView.as_view(), name='job_detail_view'),
]