from celery import shared_task
from datetime import timedelta
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_text
import logging
from ...apps.credentials.models import Credential, CREDENTIAL_STATE
from ...core.spiders.hunter import Hunter


logger = logging.getLogger(__name__)

@shared_task
def validate_targets(targets=[]):    
    if not Credential.is_available():
        return None, 'Credentials are not available'
    else:
        try:
            hunter = Hunter()
            for id in targets:
                hunter.validate(id)
            hunter.brwoser.quit(state=CREDENTIAL_STATE.active)
            return True, 'Successfully validated.'
        except Exception as e:
            print(str(e))
            return False, str(e)