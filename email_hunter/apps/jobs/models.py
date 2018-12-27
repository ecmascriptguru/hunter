from django.db import models
from model_utils.models import TimeStampedModel
from django_fsm import FSMField


class JOB_STATE:
    default = 'n'
    pending = 'p'
    in_progress = 'i'
    completed = 'c'
    got_error = 'e'
    archived = 'a'


class Job(TimeStampedModel):
    JOB_STATE_CHOICES = (
        (JOB_STATE.default, 'Default'),
        (JOB_STATE.in_progress, 'In Progress'),
        (JOB_STATE.pending, 'Pending'),
        (JOB_STATE.completed, 'Finished'),
        (JOB_STATE.got_error, 'Got an error'),
        (JOB_STATE.archived, 'Archived'),
    )

    internal_uuid = models.UUIDField(default=None, null=True, blank=True)
    state = FSMField(default=JOB_STATE.default, choices=JOB_STATE_CHOICES)
    file = models.ForeignKey('targets.TargetFile', on_delete=models.CASCADE, related_name='jobs',
                default=None, null=True, blank=True)