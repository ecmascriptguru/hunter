import itertools
import django_tables2 as tables
from .models import Credential


class CredentialTable(tables.Table):
    """Table to show credentials
    """
    row_number = tables.Column(empty_values=(), verbose_name='Number')

    class Meta:
        model = Credential
        template_name = 'django_tables2/bootstrap.html'
    
    def __init__(self, *args, **kwargs):
        super(CredentialTable, self).__init__(**kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '# %d' % (next(self.counter) + 1)