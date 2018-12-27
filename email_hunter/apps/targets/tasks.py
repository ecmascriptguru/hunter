from celery import shared_task
from datetime import timedelta
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_text
import logging
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
        target = Target.objects.get(pk=targets[0])

        hunter = Hunter(job_uuid=target.job.internal_uuid)
        for idx, id in enumerate(targets):
            result = hunter.validate(id, idx)

            # To have browser grab cookies
            if idx < len(targets) - 1:
                hunter.browser.open_gmail()
        hunter.browser.quit(state=CREDENTIAL_STATE.active)

        target = Target.objects.get(pk=targets[-1])
        job = target.job
        if job.state != JOB_STATE.completed:
            job.state = JOB_STATE.completed
            job.save()
        
        if job.file:
            file = target.job.file
            if file.state != TARGET_FILE_STATE.done:
                file.state = TARGET_FILE_STATE.done
                file.save()

        return True, 'Successfully finished.'
        # except Exception as e:
        #     print(str(e))
        #     return False, str(e)