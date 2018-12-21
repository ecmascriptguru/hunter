from celery import shared_task
from celery.contrib import rdb
from datetime import timedelta
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_text
import logging

logger = logging.getLogger(__name__)


@shared_task
def recovery_credential(credential_pk):
    from ...core.spiders.browser import Browser
    b = Browser(pk=credential_pk)
    result = b.recovery_account()
    b.quit()
    return result


@shared_task
def debug_task():
    logger.error("In celery task!")