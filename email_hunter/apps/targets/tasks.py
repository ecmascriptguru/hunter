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

        if target.file.state != TARGET_FILE_STATE.in_progress:
            target.file.state = TARGET_FILE_STATE.in_progress
            target.file.save()
        if target.job.state != JOB_STATE.in_progress:
            target.job.state = JOB_STATE.in_progress
            target.job.save()

        hunter = Hunter(job_uuid=target.job.internal_uuid)
        for idx, id in enumerate(targets):
            target = Target.objects.get(pk=id)
            target.state = TARGET_STATE.in_progress
            target.save()
            hunter.validate(id, idx)
            # To have browser grab cookies
            hunter.browser.open_gmail()
        hunter.browser.quit(state=CREDENTIAL_STATE.active)
        return True, 'Successfully finished.'
        # except Exception as e:
        #     print(str(e))
        #     return False, str(e)


@shared_task(bind=True)
def process_file(self, file_id=None):
    if file_id is None:
        raise Exception("file_id is required.")
    
    limit = 5
    if hasattr(settings, 'EMAIL_HUNTER_BATCH_SIZE'):
        limit = settings.EMAIL_HUNTER_BATCH_SIZE

    if Credential.is_available():
        file = TargetFile.objects.get(pk=file_id)
        todos = file.todos(limit)
        file.state = TARGET_FILE_STATE.in_progress
        file.save()

        todos.update(state=TARGET_STATE.pending, )
    else:
        return False, 'Credentials are not available any more...'