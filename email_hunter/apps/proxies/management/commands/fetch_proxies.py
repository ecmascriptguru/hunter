from django.conf import settings
from django.core.management import BaseCommand
from ...models import Proxy


class Command(BaseCommand):
    """
    Command to pull proxies from proxy providers and push them into database.
    """

    def handle(self, *args, **options):
        print("Done")