from django.conf import settings
from django.core.management import BaseCommand
from ...backends.fetchs import ProxyFetcher


class Command(BaseCommand):
    """
    Command to pull proxies from proxy providers and push them into database.
    """

    def handle(self, *args, **options):
        try:
            c, u = ProxyFetcher.fetch_all()
            print("{0} proxies added and {1} proxies are updated.".format(c, u))
        except Exception as e:
            print(str(e))