import itertools
import django_tables2 as tables
from django.template.loader import render_to_string
from .models import Lead


class LeadTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    url = tables.Column(empty_values=(), verbose_name='Url', orderable=False)

    class Meta:
        model = Lead
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('id', 'modified', )
        sequence = ['row_number', 'email', 'target', 'engine', 'found_by', ]

    def __init__(self, *args, **kwargs):
        super(LeadTable, self).__init__(**kwargs)
        self.counter = itertools.count()

    def render_target(self, record):
        if record.target:
            return record.target.full_name
        else:
            return 'Deleted'
    
    def render_url(self, record):
        return record.target.url
    
    def render_created(self, record):
        return record.created.strftime("%b %d, %Y")

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)