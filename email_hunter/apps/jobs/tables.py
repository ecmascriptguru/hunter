import itertools
import django_tables2 as tables
from django.template.loader import render_to_string
from .models import Job


class JobTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    actions = tables.Column(empty_values=(), orderable=False)
    actions_template = 'jobs/_job_table_actions_column.html'

    class Meta:
        model = Job
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('id', 'modified', )
        sequence = ['row_number', 'internal_uuid', 'state', ]

    def __init__(self, *args, **kwargs):
        super(JobTable, self).__init__(**kwargs)
        self.counter = itertools.count()

    def render_actions(self, record):
        return render_to_string(self.actions_template, context={'record': record})

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)