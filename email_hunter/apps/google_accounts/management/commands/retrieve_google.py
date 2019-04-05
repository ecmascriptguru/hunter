import time
from django.conf import settings
from django.core.management import BaseCommand
from email_hunter.core.spiders.backlink_hunter import BacklinkHunter as Hunter


class Command(BaseCommand):
    """
    Command to pull proxies from proxy providers and push them into database.
    """

    def handle(self, *args, **options):
        try:
            print("You'll have to login to your google account linked to Google Search Console.")
            hunter = Hunter()
            hunter.login_gmail()
            hunter.open_search_console()

            hunter.get_report()
            # print(properties)
            print("Please quit the browser once you finished what you want to do.")
            print("Or you will waste your resources of your operating system.")
            time.sleep(300)
        except Exception as e:
            print(str(e))