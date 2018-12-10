from django.db import models
from django.db.models import PositiveIntegerField
from django.core.validators import MinValueValidator, MaxValueValidator
from model_utils.models import TimeStampedModel
from django_fsm import FSMField

class Proxy(TimeStampedModel):
    """
    Credentials class, which would store google, linkedIn account and corresponding proxy
    """

    class PROVIDER:
        MY_PRIVATE_PROXY = 'MPR'

    PROVIDER_CHOICES = (
        (PROVIDER.MY_PRIVATE_PROXY, 'myprivateproxy.net'),
    )

    class STATE:
        active = 'A'
        inactive = 'I'
    
    STATE_CHOICES = (
        (STATE.active, 'Active'),
        (STATE.inactive, 'Inactive')
    )

    ip_address = models.CharField(max_length=15)
    port = models.PositiveIntegerField(default=2228,
        validators=[MinValueValidator(1), MaxValueValidator(65535)],
        help_text='Port Number of proxy')
    provider = FSMField(default=PROVIDER.MY_PRIVATE_PROXY, choices=PROVIDER_CHOICES)
    state = FSMField(default=STATE.inactive, choices=STATE_CHOICES)

    def __str__(self):
        return "{0}:{1}".format(self.ip_address, self.port)