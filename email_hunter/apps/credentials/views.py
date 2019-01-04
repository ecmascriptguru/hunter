from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.conf import settings
from django.views import generic
from django_tables2.views import SingleTableMixin
from django.contrib.auth.decorators import login_required
from .tables import CredentialTable, Credential
from .forms import CredentialUploadForm, CredentialForm


class CredentialListView(LoginRequiredMixin, SingleTableMixin, generic.ListView):
    decorators = [login_required]
    model = Credential
    table_class = CredentialTable
    template_name = 'credentials/credential_list_view.html'


class CredentialUploadView(LoginRequiredMixin, generic.FormView):
    form_class = CredentialUploadForm
    success_url = reverse_lazy('landings:dashboard_view')
    template_name = 'credentials/credential_upload_view.html'

    def form_valid(self, form, *args, **kwargs):
        file = self.request.FILES['file']
        return super().form_valid(form, *args, **kwargs)


class CredentialCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = CredentialForm
    template_name = 'credentials/credential_create_view.html'
    success_url = reverse_lazy('credentials:credential_list_view')


class CredentialUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = CredentialForm
    model = Credential
    template_name = 'credentials/credential_update_view.html'
    success_url = reverse_lazy('credentials:credential_list_view')


class CredentialDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Credential
    template_name = 'credentials/credential_delete_view.html'
    success_url = reverse_lazy('credentials:credential_list_view')