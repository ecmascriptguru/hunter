from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import BaseCommand
from email_hunter.apps.articles.models import Article, ARTICLE_STATE, Bucket, BUCKET_STATE


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not settings.DEBUG:
            raise ImproperlyConfigured('You are not able to execute this command in production.')

        count = Article.objects.filter(state__in=[ARTICLE_STATE.not_found,
            ARTICLE_STATE.no_author, ARTICLE_STATE.pending, ARTICLE_STATE.in_progress])\
            .update(state=ARTICLE_STATE.default)
        Bucket.objects.filter(state__in=[BUCKET_STATE.in_progress, BUCKET_STATE.pending])\
            .update(state=BUCKET_STATE.default)
        print("%d articles were changed to *default* state." % count)