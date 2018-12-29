import itertools
import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from .models import Job


class JobTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    progress = tables.Column(empty_values=(), verbose_name='Progress', orderable=False)
    # actions = tables.Column(empty_values=(), orderable=False)
    progress_template = 'jobs/_job_table_progress_column.html'

    class Meta:
        model = Job
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('id', 'created', )
        sequence = ['row_number', 'internal_uuid', 'file', 'state', 'progress', 'modified']

    def __init__(self, *args, **kwargs):
        super(JobTable, self).__init__(**kwargs)
        self.counter = itertools.count()
    
    def render_internal_uuid(self, record):
        return mark_safe('<a href="{0}">{1}</a>'.format(
            reverse_lazy('jobs:job_detail_view', args=(record.internal_uuid, )), record.internal_uuid))

    def render_progress(self, record):
        return render_to_string(self.progress_template, context={'record': record})

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)
    
    def render_file(self, record):
        return record.file.filename