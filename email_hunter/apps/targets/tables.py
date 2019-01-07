import itertools
import django_tables2 as tables
from django.template.loader import render_to_string
from .models import Target, TargetFile


class TargetTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    actions = tables.Column(empty_values=(), orderable=False)
    full_name = tables.Column(empty_values=(), verbose_name='Full Name', orderable=False)
    actions_template = 'targets/_target_table_actions_column.html'

    class Meta:
        model = Target
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('file', 'id', 'created', 'job', 'first_name', 'last_name', )
        sequence = ['row_number', 'full_name', 'domain', 'state', 'created_by', ]

    def __init__(self, *args, **kwargs):
        super(TargetTable, self).__init__(**kwargs)
        self.counter = itertools.count()

    def render_actions(self, record):
        return render_to_string(self.actions_template, context={'record': record})
    
    def render_full_name(self, record):
        return record.full_name

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)


class TargetFileTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    actions = tables.Column(empty_values=(), orderable=False)
    targets = tables.Column(empty_values=(), verbose_name='Targets', orderable=False)
    found_rate = tables.Column(empty_values=(), verbose_name='Found_rate', orderable=False)
    actions_template = 'targets/_target_file_table_actions_column.html'

    class Meta:
        model = TargetFile
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('internal_uuid', 'created', 'encode_type', )
        sequence = ['row_number', 'filename', 'targets', 'found_rate', 'created_by', ]

    def __init__(self, *args, **kwargs):
        super(TargetFileTable, self).__init__(**kwargs)
        self.counter = itertools.count()

    def render_targets(self, record):
        return len(record.targets.all())

    def render_found_rate(self, record):
        processed = len(record.complete_targets)
        found = len(record.validated_targets)
        if processed == 0:
            return ''
        else:
            return "{}/{} Found({:.2f}%)".format(found, processed, found/processed)

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)

    def render_actions(self, record):
        return render_to_string(self.actions_template, context={'record': record})