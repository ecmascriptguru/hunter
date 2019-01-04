from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django_tables2.config import RequestConfig
from django_tables2 import SingleTableMixin
from .models import Proxy
from .backends import ProxyFetcher
from .tables import ProxyTable


class ProxyListView(LoginRequiredMixin, SingleTableMixin, ListView):
    decorators = [login_required]
    model = Proxy
    table_class = ProxyTable
    template_name = 'proxies/proxy_list_view.html'