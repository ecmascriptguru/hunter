from django.apps import AppConfig


class LeadsConfig(AppConfig):
    name = 'email_hunter.apps.leads'

    def ready(self):
        pass