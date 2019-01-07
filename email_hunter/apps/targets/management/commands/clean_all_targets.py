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
        # if not settings.DEBUG:
        #     raise Exception('Projects is not in DEBUG mode.')

        count, info = Target.objects.all().delete()
        print("{} targets removed from database.".format(count))