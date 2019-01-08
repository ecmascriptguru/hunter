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
def validate_targets(self, targets=[], file_id=None):
    if not Credential.is_available():
        return None, 'Credentials are not available'
    else:
        job = Job.objects.create(internal_uuid=self.request.id, file_id=file_id,
                state=JOB_STATE.in_progress)
        
        if file_id is not None:
            try:
                file = TargetFile.objects.get(internal_uuid=file_id)
                if file.state != TARGET_FILE_STATE.in_progress:
                    file.state = TARGET_FILE_STATE.in_progress
                    file.save()
            except TargetFile.DoesNotExist:
                print('File not found.')

        try:
            hunter = Hunter(self, len(targets))
            for idx, id in enumerate(targets):
                    target = Target.objects.get(pk=id)
                    target.job = job
                    target.save()

            for idx, id in enumerate(targets):
                result, _ = hunter.validate(id, idx)

            return hunter.stop()
        except Exception as e:
            print(str(e))
            for idx, id in enumerate(targets):
                target = Target.objects.get(pk=id)
                if target.state in [TARGET_STATE.pending, TARGET_STATE.in_progress]:
                    target.state = TARGET_STATE.has_error
                    target.save()
            return hunter.stop(job_state=JOB_STATE.got_error)