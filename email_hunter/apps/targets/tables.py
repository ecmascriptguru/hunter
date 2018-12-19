import itertools
import django_tables2 as tables
from .models import Target, TargetFile


class TargetTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    actions = tables.Column(empty_values=(), orderable=False)

    class Meta:
        model = Target
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('file', 'id', 'modified', )
        sequence = ['row_number', 'first_name', 'last_name', 'domain', 'state', 'created_by', ]

    def __init__(self, *args, **kwargs):
        super(TargetTable, self).__init__(**kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)


class TargetFileTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    actions = tables.Column(empty_values=(), orderable=False)
    targets = tables.Column(empty_values=(), verbose_name='Count of Targets')

    class Meta:
        model = TargetFile
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('internal_uuid', 'modified', )
        sequence = ['row_number', 'filename', 'targets', 'encode_type', 'created_by', ]

    def __init__(self, *args, **kwargs):
        super(TargetFileTable, self).__init__(**kwargs)
        self.counter = itertools.count()

    def render_targets(self, record):
        return len(record.targets.all())

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)