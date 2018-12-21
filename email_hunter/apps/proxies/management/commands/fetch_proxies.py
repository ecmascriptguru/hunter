from django.conf import settings
from django.core.management import BaseCommand
from ...backends.fetchs import ProxyFetcher


class Command(BaseCommand):
    """
    Command to pull proxies from proxy providers and push them into database.
    """

    def handle(self, *args, **options):
        try:
            c, u, d = ProxyFetcher.fetch_all()
            print("""{0} proxies deleted from database.\n"""
            """{1} proxies added and {2} proxies are updated.""".format(d, c, u))
        except Exception as e:
            print(str(e))