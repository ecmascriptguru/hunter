import itertools
import django_tables2 as tables
from django.template.loader import render_to_string
from .models import Article, Bucket


class BucketTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    actions = tables.Column(empty_values=(), orderable=False)
    articles = tables.Column(empty_values=(), orderable=False)

    actions_template = 'buckets/_bucket_table_actions_column.html'

    class Meta:
        model = Bucket
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('id', 'modified', 'created', )
        sequence = ['row_number', 'name', 'articles', 'state', 'user', ]

    def __init__(self, *args, **kwargs):
        super(BucketTable, self).__init__(**kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)
    
    def render_articles(self, record):
        return len(record.ready_articles)

    def render_actions(self, record):
        return render_to_string(self.actions_template, context={'record': record})


class ArticleTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='#', orderable=False)

    class Meta:
        model = Article
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('id', 'modified', 'created', 'authors', )
        sequence = ['row_number', 'url', 'state' ]

    def __init__(self, *args, **kwargs):
        super(ArticleTable, self).__init__(**kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)