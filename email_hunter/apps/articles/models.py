from django.db import models
from model_utils.models import TimeStampedModel
from django_fsm import FSMField
from django.contrib.postgres.fields import JSONField


class BUCKET_STATE:
    default = 'r'
    pending = 'p'
    in_progress = 'i'


class Bucket(TimeStampedModel):
    BUCKET_STATE_OPTIONS = (
        (BUCKET_STATE.default, 'Ready'),
        (BUCKET_STATE.pending, 'Pending'),
        (BUCKET_STATE.in_progress, 'Processing'),
    )

    name = models.CharField(max_length=255)
    state = FSMField(default=BUCKET_STATE.default, choices=BUCKET_STATE_OPTIONS)
    user = models.ForeignKey('users.User', on_delete=models.SET_DEFAULT, related_name='buckets',
                default=None, null=True, blank=True)
    job_uuid = models.UUIDField(default=None, null=True, blank=True)
    is_test_data = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def ready_articles(self):
        return self.articles.filter(state=ARTICLE_STATE.default)
    
    @property
    def is_ready(self):
        return self.state == BUCKET_STATE.default and len(self.ready_articles) > 0
    
    @property
    def complete_articles(self):
        return self.articles.filter(state__in=[ARTICLE_STATE.found, ARTICLE_STATE.not_found, ARTICLE_STATE.need_confirm])
    
    @property
    def found_articles(self):
        return self.articles.filter(state__in=[ARTICLE_STATE.found, ARTICLE_STATE.need_confirm])

    @property
    def incorrect_urls(self):
        return self.articles.filter(state=ARTICLE_STATE.page_not_found)
    
    @property
    def odd_urls(self):
        return self.articles.filter(state=ARTICLE_STATE.no_author)
    
    @property
    def found_rate(self):
        if len(self.complete_articles) > 0:
            return "%.2f" % ((len(self.found_articles) / len(self.complete_articles)) * 100)
        else:
            return 0

class ARTICLE_STATE:
    default = 'r'
    found = 'f'
    not_found = 'n'
    pending = 'd'
    in_progress = 'i'
    need_confirm = 'c'
    page_not_found = 'p'
    has_error = 'e'
    no_author = 'b'


class Article(TimeStampedModel):
    class Meta:
        ordering = ('modified', )

    ARTICLE_STATE_OPTIONS = (
        (ARTICLE_STATE.default, 'Ready'),
        (ARTICLE_STATE.found, 'Found'),
        (ARTICLE_STATE.not_found, 'Not Found'),
        (ARTICLE_STATE.pending, 'Pending'),
        (ARTICLE_STATE.in_progress, 'In Progress'),
        (ARTICLE_STATE.need_confirm, 'Need Confirm'),
        (ARTICLE_STATE.page_not_found, 'Page Not Found'),
        (ARTICLE_STATE.no_author, 'No Author'),
        (ARTICLE_STATE.has_error, 'Error'),
    )
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE, related_name='articles')
    url = models.URLField(unique=True, verbose_name='Article URL')
    state = FSMField(default=ARTICLE_STATE.default, choices=ARTICLE_STATE_OPTIONS)
    authors = JSONField(default=None, blank=True)

    @classmethod
    def flops(cls):
        return cls.objects.filter(state__in=[ARTICLE_STATE.page_not_found, ARTICLE_STATE.has_error])
    
    @classmethod
    def not_founds(cls):
        return cls.objects.filter(state__in=[ARTICLE_STATE.not_found, ARTICLE_STATE.no_author])