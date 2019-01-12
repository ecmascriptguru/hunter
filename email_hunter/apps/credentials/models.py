from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel
from django_fsm import FSMField
from ..proxies.models import Proxy, PROXY_STATE


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
    captcha_image = models.URLField(default=None, blank=True, null=True, verbose_name='Captcha Image')
    captcha_value = models.CharField(max_length=20, default=None, blank=True, null=True)

    block_notification_email_plain_text_template_name = 'credentials/mails/credential_block_notification.txt'
    block_notification_email_html_template_name = 'credentials/mails/credential_block_notification.html'

    class Meta:
        ordering = ['modified', ]
    
    def change_proxy(self):
        self.proxy.state = PROXY_STATE.inactive
        self.proxy.save()
        self.proxy = Proxy.get_active()
        return self.save()

    @classmethod
    def actives(cls):
        return cls.objects.filter(state=CREDENTIAL_STATE.active)

    @classmethod
    def get_active(cls):
        return cls.actives().first()

    @classmethod
    def holds(cls):
        return cls.objects.filter(state=CREDENTIAL_STATE.hold)

    @classmethod
    def get_hold(cls):
        return cls.holds().first()

    @classmethod
    def no_proxies(cls):
        return cls.objects.filter(state=CREDENTIAL_STATE.no_proxy)

    @classmethod
    def get_no_proxy(cls):
        return cls.no_proxies().first()
    
    @classmethod
    def is_available(cls):
        return cls.actives().exists()
    
    def to_json(self, with_proxy=False):
        result = {
            'pk': self.pk,
            'email': self.email,
            'password': self.password
        }

        if with_proxy:
            result['proxy'] = self.proxy.to_json()
        
        return result