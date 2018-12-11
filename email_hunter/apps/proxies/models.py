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


class PROXY_TYPE:
    dedicated = 'D'
    shared = 'S'


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
    
    TYPE_CHOICES = (
        (PROXY_TYPE.dedicated, 'Dedicated'),
        (PROXY_TYPE.shared, 'Shared'),
    )

    ip_address = models.CharField(max_length=15)
    port = models.PositiveIntegerField(default=2228,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
        help_text='Port Number of proxy')
    provider = FSMField(default=PROXY_PROVIDER.MY_PRIVATE_PROXY, choices=PROVIDER_CHOICES)
    proxy_type = FSMField(default=PROXY_TYPE.shared, choices=TYPE_CHOICES)
    state = FSMField(default=PROXY_STATE.inactive, choices=STATE_CHOICES)

    def __str__(self):
        return "{0}:{1}".format(self.ip_address, self.port)