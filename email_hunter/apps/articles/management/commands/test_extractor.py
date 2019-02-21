import random
import time
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import BaseCommand
from email_hunter.core.spiders.browser import Chrome as Browser
from email_hunter.core.spiders.author_extractor import AuthorHunter as Hunter
from ...tasks import extract_authors
from ...models import Article


class Command(BaseCommand):
    """
    Command to extract author from a failed article
    """

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise ImproperlyConfigured('You are not able to execute this command in production.')

        if Article.flops().exists():
            article = random.choice(Article.not_founds())# .first()
            hunter = Hunter(article.url)
            browser = Browser()
            try:
                browser.get(article.url)
                time.sleep(2)
                hunter.download(input_html=browser.page_source)
                hunter.parse()
                print(article.url)
                print(hunter.authors)
            except Exception as e:
                print(str(e))
            finally:
                browser.quit()
        else:
            print("No available article found.")