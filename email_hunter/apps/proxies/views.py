from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Proxy
from .backends import ProxyFetcher


class ProxyListView(ListView):
    decorators = [login_required]
    model = Proxy
    template_name = 'proxies/proxy_list_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProxyListView, self).get_context_data(*args, *kwargs)
        temp = ProxyFetcher.fetch_myprivateproxy_proxies()
        return context