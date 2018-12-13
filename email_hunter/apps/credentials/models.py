from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel
from django_fsm import FSMField
from ..proxies.models import Proxy


class CREDENTIAL_STATE:
    """Credential's states
    """
    no_proxy = 'n'
    active = 'a'
    hold = 'h'
    processing = 'p'
    using = 'u'

class Credential(TimeStampedModel):
    """Model to store google and linkedIn account
    """
    
    CREDENTIAL_STATE_CHOICES = (
        (CREDENTIAL_STATE.no_proxy, 'No proxy'),
        (CREDENTIAL_STATE.active, 'Active'),
        (CREDENTIAL_STATE.hold, 'Hold'),
        (CREDENTIAL_STATE.processing, 'Processing'),
        (CREDENTIAL_STATE.using, 'Using'),
    )

    proxy = models.OneToOneField(Proxy, related_name='credential', on_delete=models.SET_NULL, blank=True, null=True)
    email = models.EmailField(max_length=128, unique=True, default=None, null=False, blank=False)
    password = models.CharField(max_length=128, default=None)
    recovery_email = models.EmailField(max_length=128, default=settings.DEFAULT_RECOVERY_EMAIL)
    recovery_phone = models.CharField(max_length=15, null=False, blank=False, 
                            default=settings.DEFAULT_RECOVERY_PHONE)
    has_linkedin = models.BooleanField(default=False)
    state = FSMField(default=CREDENTIAL_STATE.no_proxy, choices=CREDENTIAL_STATE_CHOICES)