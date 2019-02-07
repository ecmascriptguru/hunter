from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersConfig(AppConfig):
    name = 'email_hunter.apps.users'
    verbose_name = _('users')

    def ready(self):
        import email_hunter.apps.users.signals