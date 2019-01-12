from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CredentialsConfig(AppConfig):
    name = 'email_hunter.apps.credentials'
    verbose_name = _('credentials')

    def ready(self):
        import email_hunter.apps.credentials.signals
