from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Proxy

class ProxyListView(ListView):
    decorators = [login_required]
    model = Proxy
    template_name = 'proxies/proxy_list_view.html'