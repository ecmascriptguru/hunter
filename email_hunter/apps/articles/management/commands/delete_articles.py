from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import BaseCommand
from email_hunter.apps.articles.models import Article, Bucket


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not settings.DEBUG:
            raise ImproperlyConfigured('You are not able to execute this command in production.')
        
        print(Bucket.objects.filter(is_test_data=True).delete())