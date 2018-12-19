from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.conf import settings
from django.views import generic
from django_tables2.views import SingleTableMixin
from django.contrib.auth.decorators import login_required
from .tables import CredentialTable, Credential
from .forms import CredentialUploadForm, CredentialForm


class CredentialListView(SingleTableMixin, generic.ListView):
    decorators = [login_required]
    model = Credential
    table_class = CredentialTable
    template_name = 'credentials/credential_list_view.html'


class CredentialUploadView(generic.FormView):
    form_class = CredentialUploadForm
    success_url = reverse_lazy('landings:dashboard_view')
    template_name = 'credentials/credential_upload_view.html'

    def form_valid(self, form, *args, **kwargs):
        file = self.request.FILES['file']
        return super().form_valid(form, *args, **kwargs)


class CredentialCreateView(generic.CreateView):
    form_class = CredentialForm
    template_name = 'credentials/credential_create_view.html'
    success_url = reverse_lazy('credentials:credential_list_view')