from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django_tables2.views import SingleTableMixin
from .models import Target, TargetFile
from .forms import TargetUploadForm, TargetUpdateForm, TargetFileForm
from .tables import TargetTable, TargetFileTable


class TargetListView(LoginRequiredMixin, SingleTableMixin, generic.ListView):
    decorators = [login_required]
    model = Target
    template_name = 'targets/target_list_view.html'
    table_class = TargetTable


class FileListView(LoginRequiredMixin, SingleTableMixin, generic.ListView):
    model = TargetFile
    template_name = 'targets/target_file_list_view.html'
    table_class = TargetFileTable


class FileUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = TargetFileForm
    template_name = 'targets/target_file_start_view.html'
    success_url = reverse_lazy('jobs:job_list_view')

    def get_object(self):
        return TargetFile.objects.get(pk=self.kwargs.get('pk'))


class FileDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'targets/target_file_detail_view'

    def get_object(self):
        return TargetFile.objects.get(pk=self.kwargs.get('pk'))


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


class TargetUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = TargetUpdateForm
    success_url = reverse_lazy('targets:target_list_view')
    template_name = 'targets/target_update_view.html'
    model = Target