from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import GoogleAccount


class GoogleAccountAdmin(ModelAdmin):
    list_display = ('email', 'password', 'proxy', )
    class Meta:
        model = GoogleAccount

admin.site.register(GoogleAccount, GoogleAccountAdmin)
