import itertools
import django_tables2 as tables
from .models import Proxy

class ProxyTable(tables.Table):
    class Meta:
        model = Proxy
        template_name = 'django_tables2/bootstrap.html'
        exclude = ('id', 'external_plan_id', 'ip_address', 'port', 'created', )
        sequence = ('row_number', 'proxy', 'plan_type', 'provider', 'state', )
    
    row_number = tables.Column(empty_values=(), verbose_name='Number')
    proxy = tables.Column(empty_values=())

    def __init__(self, *args, **kwargs):
        super(ProxyTable, self).__init__(**kwargs)
        self.counter = itertools.count()

    def render_row_number(self):
        return '# %d' % (next(self.counter) + 1)
    
    def render_proxy(self, record):
        return "{0}:{1}".format(record.ip_address, record.port)
    
    def render_modified(self, record):
        return record.modified.strftime('%b %d, %Y')