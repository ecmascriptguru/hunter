from django.contrib import admin
from django.urls import path, include
from django.template.response import TemplateResponse
from .models import Credential


class CrednetialAdmin(admin.ModelAdmin):
    exclude = ('captcha_image',)


admin.site.register(Credential, CrednetialAdmin)