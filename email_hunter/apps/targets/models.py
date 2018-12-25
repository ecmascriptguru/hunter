import uuid
from django.db import models
from model_utils.models import TimeStampedModel
from django_fsm import FSMField
from ...apps.users.models import User
from ...apps.jobs.models import Job, JOB_STATE


class ENCODE_TYPE:
    unicode = 'utf-8'
    latin1 = 'latin-1'
    cp1252 = 'cp1252'


class TargetFile(TimeStampedModel):
    ENCODE_TYPE_CHOICES = (
        (ENCODE_TYPE.unicode, 'UTF-8'),
        (ENCODE_TYPE.latin1, 'Latin'),
        (ENCODE_TYPE.cp1252, 'CP 1252'),
    )
    internal_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=128, null=True)
    encode_type = FSMField(default=ENCODE_TYPE.unicode, choices=ENCODE_TYPE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='target_files')


class TARGET_STATE:
    to_do = 't'
    in_progress = 'p'
    validated = 'v'
    failed = 'f'
    has_error = 'e'


class Target(TimeStampedModel):
    TARGET_STATE_CHOICES = (
        (TARGET_STATE.to_do, 'TO DO'),
        (TARGET_STATE.in_progress, 'In Progress'),
        (TARGET_STATE.validated, 'Found'),
        (TARGET_STATE.failed, 'Not Found'),
        (TARGET_STATE.has_error, 'Got Error'),
    )

    file = models.ForeignKey(TargetFile, on_delete=models.SET_NULL, null=True, related_name='targets')
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    domain = models.CharField(max_length=60)
    state = FSMField(default=TARGET_STATE.to_do, choices=TARGET_STATE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='targets')
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='targets')

    class Meta:
        unique_together = (('first_name', 'last_name', 'domain',),)

    @classmethod
    def todos(cls):
        return cls.objects.filter(state__in=[TARGET_STATE.to_do, TARGET_STATE.has_error])