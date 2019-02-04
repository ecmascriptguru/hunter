import uuid
from django.db import models
from django.utils.text import Truncator
from model_utils.models import TimeStampedModel
from django_fsm import FSMField
from ...apps.jobs import JOB_STATE
from . import ENCODE_TYPE


class TARGET_STATE:
    to_do = 't'
    pending = 'p'
    in_progress = 'i'
    validated = 'v'
    failed = 'f'
    has_error = 'e'


class TARGET_FILE_STATE:
    default = 'n'
    pending = 'p'
    in_progress = 'i'
    done = 'd'
    archived = 'a'


class TargetFile(TimeStampedModel):
    ENCODE_TYPE_CHOICES = (
        (ENCODE_TYPE.unicode, 'UTF-8'),
        (ENCODE_TYPE.latin1, 'Latin'),
        (ENCODE_TYPE.cp1252, 'CP 1252'),
    )

    TARGET_FILE_STATE_CHOICES = (
        (TARGET_FILE_STATE.default, 'Normal'),
        (TARGET_FILE_STATE.pending, 'Pending'),
        (TARGET_FILE_STATE.in_progress, 'In Progress'),
        (TARGET_FILE_STATE.done, 'Done'),
        (TARGET_FILE_STATE.archived, 'Archived'),
    )
    internal_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=128, null=True)
    encode_type = FSMField(default=ENCODE_TYPE.unicode, choices=ENCODE_TYPE_CHOICES)
    state = FSMField(default=TARGET_FILE_STATE.default,
                        choices=TARGET_FILE_STATE_CHOICES)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True,
                        related_name='target_files')

    def todos(self, limit=None):
        qs = self.targets.filter(state__in=[TARGET_STATE.to_do, TARGET_STATE.has_error])
        if limit:
            return qs[:limit]
        else:
            return qs
    
    def __str__(self):
        return Truncator(self.filename).chars(24)
    
    @property
    def pending_targets(self):
        return self.targets.filter(state=TARGET_STATE.pending)
    
    @property
    def doing_targets(self):
        return self.targets.filter(state=TARGET_STATE.in_progress)
    
    @property
    def complete_targets(self):
        return self.targets.filter(state__in=[TARGET_STATE.validated, TARGET_STATE.failed])
    
    @property
    def validated_targets(self):
        return self.targets.filter(state=TARGET_STATE.validated)

    @property
    def is_ready(self):
        return self.state in [TARGET_FILE_STATE.default, TARGET_FILE_STATE.done] and len(self.todos()) > 0
    
    @property
    def is_pending_or_in_progress(self):
        return self.state in [TARGET_FILE_STATE.pending, TARGET_FILE_STATE.in_progress]
    
    @property
    def has_pending_or_in_progress_jobs(self):
        return len(self.jobs.filter(state__in=[JOB_STATE.pending, JOB_STATE.in_progress])) > 0
    
    @property
    def jobs_in_queue(self):
        return self.jobs.filter(state__in=[JOB_STATE.pending, JOB_STATE.in_progress])
    
    @classmethod
    def availables(cls):
        return cls.objects.filter(state__in=[TARGET_FILE_STATE.default, TARGET_FILE_STATE.done])


class Target(TimeStampedModel):
    TARGET_STATE_CHOICES = (
        (TARGET_STATE.to_do, 'TO DO'),
        (TARGET_STATE.pending, 'Pending'),
        (TARGET_STATE.in_progress, 'In Progress'),
        (TARGET_STATE.validated, 'Found'),
        (TARGET_STATE.failed, 'Not Found'),
        (TARGET_STATE.has_error, 'Got Error'),
    )

    file = models.ForeignKey(TargetFile, on_delete=models.SET_NULL, null=True, related_name='targets')
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    domain = models.CharField(max_length=60)
    url = models.URLField(default=None, null=True, blank=True)
    state = FSMField(default=TARGET_STATE.to_do, choices=TARGET_STATE_CHOICES)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='targets')
    job = models.ForeignKey('jobs.Job', on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name='targets')

    class Meta:
        unique_together = (('first_name', 'last_name', 'domain',),)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    @classmethod
    def todos(cls):
        return cls.objects.filter(state__in=[TARGET_STATE.to_do, TARGET_STATE.has_error])
    
    def __str__(self):
        return "{} {}({})".format(self.first_name, self.last_name, self.domain)