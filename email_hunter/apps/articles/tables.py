import itertools
import django_tables2 as tables
from django.template.loader import render_to_string
from .models import Article


class ArticleTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='#', orderable=False)

    class Meta:
        model = Article
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('id', 'modified', 'created', )
        sequence = ['row_number', 'url', 'state' ]

    def __init__(self, *args, **kwargs):
        super(ArticleTable, self).__init__(**kwargs)
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