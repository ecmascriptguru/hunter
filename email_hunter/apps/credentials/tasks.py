from celery import shared_task
from datetime import timedelta
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_text
import logging

logger = logging.getLogger(__name__)


@shared_task
def debug_task():
    logger.error("In celery task!")