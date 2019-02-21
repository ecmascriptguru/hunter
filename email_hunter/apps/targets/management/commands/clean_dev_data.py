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

        leads_count, _ = Lead.objects.all().delete()
        targets_count = Target.objects.all().exclude(state=TARGET_STATE.to_do).update(state=TARGET_STATE.to_do)
        credentials_count = Credential.objects.filter(state__in=[CREDENTIAL_STATE.processing, 
                CREDENTIAL_STATE.using, CREDENTIAL_STATE.hold]).update(state=CREDENTIAL_STATE.active)
        target_files_count = TargetFile.objects.filter(state__in=[TARGET_FILE_STATE.pending, TARGET_FILE_STATE.in_progress])\
                .update(state=TARGET_FILE_STATE.done)
        jobs_count = Job.objects.filter(state__in=[JOB_STATE.pending, JOB_STATE.in_progress])\
                .update(state=JOB_STATE.completed)
        
        print("{} leads were removded from database.".format(leads_count))
        print("{} targets were updated.".format(targets_count))
        print("{} credentials were rolled back in database.".format(credentials_count))
        print("{} jobs were marked as completed from database.".format(jobs_count))