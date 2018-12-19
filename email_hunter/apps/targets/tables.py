import itertools
import django_tables2 as tables
from .models import Target


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