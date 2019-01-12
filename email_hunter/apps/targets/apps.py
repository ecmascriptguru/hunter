from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TargetsConfig(AppConfig):
    name = 'email_hunter.apps.targets'
    verbose_name = _('targets')