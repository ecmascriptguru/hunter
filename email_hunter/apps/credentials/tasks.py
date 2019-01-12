from celery import shared_task
from celery.contrib import rdb
from datetime import timedelta
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_text
from django.core.mail import mail_admins
import logging
from ...apps.credentials.models import CREDENTIAL_STATE
from ...core.spiders.browser import Browser


logger = logging.getLogger(__name__)


@shared_task
def recovery_credential(credential_pk):    
    b = Browser(pk=credential_pk)
    state = CREDENTIAL_STATE.hold
    try:
        result = b.recovery_account()
        if result:
            state = CREDENTIAL_STATE.active
        else:
            state = CREDENTIAL_STATE.hold
    except Exception as e:
        print(str(e))
    finally:
        b.quit(state=state)
    return state


@shared_task
def send_mail_to_admins(subject, text_template, context, html_template=None):
    """Send mail to site admins
    - subject : string (required)
    - text_template : *.txt template file name (required)
    """
    message = render_to_string(text_template, context=context)
    html_message = None
    if html_template is not None and context is not None:
        html_message = render_to_string(html_template, context=context)
    mail_admins(subject, message, html_message)