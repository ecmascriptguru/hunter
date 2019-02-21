import itertools
import django_tables2 as tables
from django.template.loader import render_to_string
from .models import Article, Bucket, BUCKET_STATE


class BucketTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    found_rate = tables.Column(empty_values=(), verbose_name='Found Rate', orderable=False)
    actions = tables.Column(empty_values=(), orderable=False)
    articles = tables.Column(empty_values=(), orderable=False)

    state_template = 'buckets/_bucket_table_state_column.html'
    actions_template = 'buckets/_bucket_table_actions_column.html'

    class Meta:
        model = Bucket
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('id', 'modified', 'created', 'jobs', )
        sequence = ['row_number', 'name', 'articles', 'state', 'user', ]

    def __init__(self, *args, **kwargs):
        super(BucketTable, self).__init__(**kwargs)
        self.counter = itertools.count()
    
    def render_found_rate(self, record):
        return "{}%".format(record.found_rate)

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)
    
    def render_articles(self, record):
        return len(record.ready_articles)

    def render_actions(self, record):
        return render_to_string(self.actions_template, context={'record': record})


class ArticleTable(tables.Table):
    row_number = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    given_author = tables.Column(empty_values=(), verbose_name='Given Author', orderable=False)
    found_authors = tables.Column(empty_values=(), verbose_name='Found Authors', orderable=False)

    class Meta:
        model = Article
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('id', 'modified', 'created', 'authors', )
        sequence = ['row_number', 'url', 'state' ]

    def __init__(self, *args, **kwargs):
        super(ArticleTable, self).__init__(**kwargs)
        self.counter = itertools.count()

    def render_given_author(self, record):
        if record.bucket.is_test_data and record.authors.get('origin'):
            return record.authors.get('origin')
        else:
            ''
    
    def render_found_authors(self, record):
        if record.authors.get('found'):
            return record.authors.get('found')
        else:
            return ','.join(record.authors.get('candidates', []))

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)