from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2.views import SingleTableMixin
from .models import Job, JOB_STATE
from .tables import JobTable


class JobListView(LoginRequiredMixin, SingleTableMixin, generic.ListView):
    model = Job
    template_name = 'jobs/job_list_view.html'
    table_class = JobTable


class JobDetailView(LoginRequiredMixin, generic.DetailView):
    model = Job
    template_name = 'jobs/job_detail_view.html'