from django.db import models
from model_utils.models import TimeStampedModel
from django_fsm import FSMField


class LEAD_FOUND_ENGING:
    gplus = 'g'
    linkedin = 'l'

class Lead(TimeStampedModel):
    LEAD_FOUND_ENGING_OPTIONS = (
        (LEAD_FOUND_ENGING.gplus, 'Google+'),
        (LEAD_FOUND_ENGING.linkedin, 'LinkedIn'),
    )

    email = models.EmailField(unique=True)
    target = models.OneToOneField('targets.Target', on_delete=models.SET_NULL, related_name='lead',
            default=None, null=True, blank=True)
    engine = FSMField(default=LEAD_FOUND_ENGING.gplus, choices=LEAD_FOUND_ENGING_OPTIONS)
    profile = models.URLField()
    found_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, related_name='leads',
            default=None, null=True, blank=True, verbose_name='Found By')