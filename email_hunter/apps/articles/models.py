from django.db import models
from model_utils.models import TimeStampedModel
from django_fsm import FSMField
from django.contrib.postgres.fields import JSONField


class ARTICLE_STATE:
    default = 'r'
    found = 'f'
    not_found = 'n'
    pending = 'd'
    in_progress = 'i'
    need_confirm = 'c'
    page_not_found = 'p'
    has_error = 'e'


class Article(TimeStampedModel):
    ARTICLE_STATE_OPTIONS = (
        (ARTICLE_STATE.default, 'Ready'),
        (ARTICLE_STATE.found, 'Found'),
        (ARTICLE_STATE.not_found, 'Not Found'),
        (ARTICLE_STATE.pending, 'Pending'),
        (ARTICLE_STATE.in_progress, 'In Progress'),
        (ARTICLE_STATE.need_confirm, 'Need Confirm'),
        (ARTICLE_STATE.page_not_found, 'Page Not Found'),
        (ARTICLE_STATE.has_error, 'Error'),
    )

    url = models.URLField(unique=True, verbose_name='Article URL')
    state = FSMField(default=ARTICLE_STATE.default, choices=ARTICLE_STATE_OPTIONS)
    authors = JSONField(default=None, blank=True)