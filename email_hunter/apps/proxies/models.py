from django.db import models
from django.db.models import PositiveIntegerField
from django.core.validators import MinValueValidator, MaxValueValidator
from model_utils.models import TimeStampedModel
from django_fsm import FSMField


class PROXY_PROVIDER:
    MY_PRIVATE_PROXY = 'MPR'


class PROXY_STATE:
    active = 'A'
    inactive = 'I'


class PROXY_PLAN_TYPE:
    shared = 'S'
    dedicated = 'D'

class Proxy(TimeStampedModel):
    """
    Credentials class, which would store google, linkedIn account and corresponding proxy
    """

    PROVIDER_CHOICES = (
        (PROXY_PROVIDER.MY_PRIVATE_PROXY, 'myprivateproxy.net'),
    )
    
    STATE_CHOICES = (
        (PROXY_STATE.active, 'Active'),
        (PROXY_STATE.inactive, 'Inactive')
    )

    PROXY_PLAN_TYPE_CHOICES = (
        (PROXY_PLAN_TYPE.shared, 'Shared'),
        (PROXY_PLAN_TYPE.dedicated, 'Dedicated'),
    )
    
    ip_address = models.CharField(max_length=15)
    port = models.PositiveIntegerField(default=2228,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
        help_text='Port Number of proxy')
    provider = FSMField(default=PROXY_PROVIDER.MY_PRIVATE_PROXY, choices=PROVIDER_CHOICES)
    external_plan_id = models.CharField(max_length=32)
    plan_type = FSMField(default=PROXY_PLAN_TYPE.shared, choices=PROXY_PLAN_TYPE_CHOICES)
    state = FSMField(default=PROXY_STATE.inactive, choices=STATE_CHOICES)

    def __str__(self):
        return "{0}:{1}".format(self.ip_address, self.port)