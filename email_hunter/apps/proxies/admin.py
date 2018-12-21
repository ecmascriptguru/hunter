from functools import update_wrapper
from django.shortcuts import render_to_response
from django.conf.urls import url
from django.contrib import admin
from django.template import RequestContext
from .models import Proxy


class ProxyAdmin(admin.ModelAdmin):
    upload_template = 'proxies/admin/upload.html'

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        urls = super().get_urls()

        info = self.model._meta.app_label, self.model._meta.model_name

        my_urls = [
            url(r'upload/$', wrap(self.upload), name='%s_%s_upload' % info),
        ]

        return my_urls + urls
    
    def upload(self, request):

        return render_to_response(self.upload_template, {
            'title': 'Upload proxies',
            'opts': self.model._meta,
        })




admin.site.register(Proxy, ProxyAdmin)