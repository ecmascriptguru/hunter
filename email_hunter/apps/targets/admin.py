from django.contrib import admin
from .models import Target, TargetFile


class TargetFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'targets_count')

    def targets_count(self, obj):
        return len(obj.targets.all())

admin.site.register(Target)
admin.site.register(TargetFile, TargetFileAdmin)