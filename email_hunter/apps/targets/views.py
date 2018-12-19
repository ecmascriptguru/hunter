from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django_tables2.views import SingleTableMixin
from .models import Target
from .forms import TargetUploadForm
from .tables import TargetTable


class TargetListView(SingleTableMixin, generic.ListView):
    decorators = [login_required]
    model = Target
    template_name = 'targets/target_list_view.html'
    table_class = TargetTable


class TargetUploadView(LoginRequiredMixin, generic.FormView):
    form_class = TargetUploadForm
    template_name = 'targets/target_upload_view.html'
    success_url = reverse_lazy('targets:target_list_view')

    def form_valid(self, form):
        form.save()
        return super(TargetUploadView, self).form_valid(form)
    
    def get_form_kwargs(self, *args, **kwargs):
        params = super(TargetUploadView, self).get_form_kwargs(*args, **kwargs)
        params['user'] = self.request.user
        return params