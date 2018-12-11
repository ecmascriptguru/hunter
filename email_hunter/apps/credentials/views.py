from django.shortcuts import render
from django.views.generic import ListView
from django_tables2.views import SingleTableMixin
from django.contrib.auth.decorators import login_required
from .tables import CredentialTable, Credential


class CredentialListView(SingleTableMixin, ListView):
    decorators = [login_required]
    model = Credential
    table_class = CredentialTable
    template_name = 'credentials/credential_list_view.html'