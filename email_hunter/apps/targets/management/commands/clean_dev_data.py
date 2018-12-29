from django.conf import settings
from django.core.management import BaseCommand
from ...models import Target, TARGET_STATE, TargetFile, TARGET_FILE_STATE
from ....leads.models import Lead
from ....credentials.models import Credential, CREDENTIAL_STATE
from ....jobs.models import Job, JOB_STATE


class Command(BaseCommand):
    """
    Command to pull proxies from proxy providers and push them into database.
    """

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise Exception('Projects is not in DEBUG mode.')

        Lead.objects.all().delete()
        Target.objects.all().update(state=TARGET_STATE.to_do)
        Credential.objects.filter(state__in=[CREDENTIAL_STATE.processing, 
                CREDENTIAL_STATE.using, CREDENTIAL_STATE.hold]).update(state=CREDENTIAL_STATE.active)
        TargetFile.objects.filter(state__in=[TARGET_FILE_STATE.pending, TARGET_FILE_STATE.in_progress])\
                .update(state=TARGET_FILE_STATE.done)
        Job.objects.filter(state__in=[JOB_STATE.pending, JOB_STATE.in_progress])\
                .update(state=JOB_STATE.completed)