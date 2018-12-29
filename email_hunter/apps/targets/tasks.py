from celery import shared_task
from datetime import timedelta
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_text
import logging, time
from ...apps.credentials.models import Credential, CREDENTIAL_STATE
from ...apps.targets.models import Target, TargetFile, TARGET_STATE, TARGET_FILE_STATE
from ...apps.jobs.models import Job, JOB_STATE
from ...core.spiders.hunter import Hunter


logger = logging.getLogger(__name__)

@shared_task(bind=True)
def validate_targets(self, targets=[]):
    if not Credential.is_available():
        return None, 'Credentials are not available'
    else:
        # try:
        hunter = Hunter(self, len(targets))
        # Wait for job to be initiated.
        time.sleep(1)
        target = Target.objects.get(pk=targets[0])
        hunter.set_job(target.job.internal_uuid)
        for idx, id in enumerate(targets):
            result, lead = hunter.validate(id, idx)
        
        meta =  hunter.default_meta
        return hunter.stop()
        # except Exception as e:
        #     print(str(e))
        #     return False, str(e)