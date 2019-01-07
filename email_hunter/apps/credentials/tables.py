import itertools
from django.utils.html import format_html
from django.template.loader import render_to_string
import django_tables2 as tables
from .models import Credential


class CredentialTable(tables.Table):
    """Table to show credentials
    """
    row_number = tables.Column(empty_values=(), verbose_name='#', orderable=False)
    actions = tables.Column(empty_values=(), orderable=False, exclude_from_export=True)
    actions_template = 'credentials/_credential_table_actions_column.html'

    class Meta:
        model = Credential
        template_name = 'django_tables2/bootstrap.html'
        exclude = ['id', 'created', 'captcha_image', 'captcha_value', ]
        sequence = ['row_number', 'email', 'password', 'proxy', 'has_linkedin', 'recovery_email', 'recovery_phone', 'state']
    
    def __init__(self, *args, **kwargs):
        super(CredentialTable, self).__init__(**kwargs)
        self.counter = itertools.count()
    
    def render_actions(self, record):
        return render_to_string(self.actions_template, context={'record': record})

    def render_row_number(self):
        return '%d' % (next(self.counter) + 1)

    def render_modified(self, record):
        return record.modified.strftime('%b %d, %Y')