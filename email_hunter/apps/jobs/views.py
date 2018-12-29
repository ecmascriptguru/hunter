from datetime import timedelta
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2.views import SingleTableMixin
from django.utils import timezone
from ...apps.targets.tasks import validate_targets
from .models import Job, JOB_STATE
from .tables import JobTable
from .forms import JobForm


class JobListView(LoginRequiredMixin, SingleTableMixin, generic.ListView):
    model = Job
    template_name = 'jobs/job_list_view.html'
    ajax_template_name = 'jobs/_job_list_table.html'
    table_class = JobTable

    def get_queryset(self, *args, **kwargs):
        qs = super(JobListView, self).get_queryset(*args, **kwargs)
        offset = timezone.now() - timedelta(minutes=2)
        if self.request.is_ajax():
            self.template_name = self.ajax_template_name
        return qs.exclude(state=JOB_STATE.archived)\
                .exclude(state=JOB_STATE.completed, modified__lt=offset)


class JobDetailView(LoginRequiredMixin, generic.UpdateView):
    form_class = JobForm
    template_name = 'jobs/job_update_view.html'
    ajax_template_name = 'jobs/_job_detail.html'
    success_url = reverse_lazy('jobs:job_list_view')

    def get_object(self):
        if self.request.is_ajax():
            self.template_name = self.ajax_template_name
        return Job.objects.get(internal_uuid=self.kwargs.get('pk'))
    
    def get_context_data(self, *args, **kwargs):
        params = super(JobDetailView, self).get_context_data(*args, **kwargs)
        item = self.get_object()
        params['task'] = validate_targets.AsyncResult(str(item.internal_uuid))
        return params