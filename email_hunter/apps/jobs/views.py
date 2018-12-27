from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2.views import SingleTableMixin
from .models import Job, JOB_STATE
from .tables import JobTable
from .forms import JobForm


class JobListView(LoginRequiredMixin, SingleTableMixin, generic.ListView):
    model = Job
    template_name = 'jobs/job_list_view.html'
    table_class = JobTable

    def get_queryset(self, *args, **kwargs):
        qs = super(JobListView, self).get_queryset(*args, **kwargs)
        return qs.exclude(state=JOB_STATE.archived)


class JobDetailView(LoginRequiredMixin, generic.UpdateView):
    form_class = JobForm
    template_name = 'jobs/job_update_view.html'
    success_url = reverse_lazy('jobs:job_list_view')

    def get_object(self):
        return Job.objects.get(internal_uuid=self.kwargs.get('pk'))