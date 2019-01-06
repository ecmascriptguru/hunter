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
        hunter = Hunter(self, len(targets))
        try:
            for idx, id in enumerate(targets):
                    target = Target.objects.get(pk=id)
                    target.job = job
                    target.save()

            for idx, id in enumerate(targets):
                result, _ = hunter.validate(id, idx)

                return hunter.stop()
        except Exception as e:
            print(str(e))
            return False, str(e)