from django.conf import settings
from django.core.management import BaseCommand
from ...tasks import extract_authors
from ...models import Article


class Command(BaseCommand):
    """
    Command to extract author from a failed article
    """

    def handle(self, *args, **options):
        if Article.flops().exists():
            article = Article.flops().first()
            print(article.pk, article.state)
            print(extract_authors.delay(article.bucket.id, [article.id]))
        else:
            print("No available article found.")