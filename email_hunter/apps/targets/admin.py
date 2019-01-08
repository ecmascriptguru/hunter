from django.contrib import admin
from .models import Target, TargetFile


class TargetFileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in TargetFile._meta.get_fields() if not f.one_to_many]

admin.site.register(Target)
admin.site.register(TargetFile, TargetFileAdmin)