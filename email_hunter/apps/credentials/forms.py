import logging
from django import forms
from crispy_forms.layout import Layout, Submit, ButtonHolder, Field, Fieldset, Div, HTML
from crispy_forms.helper import FormHelper
from django_fsm import FSMField
from .models import Credential, CREDENTIAL_STATE
from ...core.widgets.fields import BasicBootstrapFormField
from ..proxies.models import Proxy
from .tasks import recovery_credential
from ...core.utils.parsers import parse_credentials
from ...apps.targets.models import ENCODE_TYPE


logger = logging.getLogger(__name__)

class CredentialUploadForm(forms.Form):
    ENCODE_TYPE_CHOICES = (
        (ENCODE_TYPE.unicode, 'UTF-8'),
        (ENCODE_TYPE.latin1, 'Latin'),
        (ENCODE_TYPE.cp1252, 'CP 1252'),
    )

    file = forms.FileField(help_text='Choose a credentials file.')
    encode_type = forms.ChoiceField(initial=ENCODE_TYPE.unicode, choices=ENCODE_TYPE_CHOICES)

    def __init__(self, *args, **kwargs):
        super(CredentialUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            BasicBootstrapFormField('file'),
            BasicBootstrapFormField('encode_type'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-primary pull-right'),
                wrapper_class='form-group',
            ),
        )

    def clean_encode_type(self):
        return self.data['encode_type']

    def clean_file(self, *args, **kwargs):
        file = self.cleaned_data['file']
        _, msg, rows = parse_credentials(file, self.clean_encode_type())
        if not _:
            if not self.errors['file']:
                self.errors['file'] = list()
            self.errors['file'].append(msg)
        else:
            credentials = list()
            for row in rows:
                email=row.get("email", "")
                
                if Credential.objects.filter(email=email).exists():
                    continue
                else:
                    row.pop('Index')
                    proxy = row.pop('proxy')
                    [ip, port] = proxy.split(':')
                    row['proxy'] = {'ip_address': ip, 'port': port}
                    if row.get('recovery_phone') is not None and\
                        not str(row['recovery_phone']).startswith('+'):
                        row['recovery_phone'] = '+' + str(row['recovery_phone'])
                    credentials.append(row)
            
            if len(credentials) == 0:
                if not self.errors.get('file', None):
                    self.errors['file'] = list()
                self.errors['file'].append('This file doesn\'t have any new credential. Choose another file...')
            else:
                self.cleaned_data['new_credentials'] = credentials
        return file
    
    def save(self, commit=True):
        for cred in self.cleaned_data['new_credentials']:
            proxy = None
            if cred.get('proxy') is not None:
                proxy, created = Proxy.objects.get_or_create(**(cred.pop('proxy')))

            credential = Credential.objects.create(**cred)
            if proxy is not None and not hasattr(proxy, 'credential'):
                credential.proxy = proxy
                credential.state = CREDENTIAL_STATE.hold
            else:
                credential.state = CREDENTIAL_STATE.no_proxy
            
            credential.save()


class CredentialForm(forms.ModelForm):
    class Meta:
        model = Credential
        exclude = ('recovery_email', 'recovery_phone', 'state', 'captcha_image')
    
    def __init__(self, *args, **kwargs):
        super(CredentialForm, self).__init__(*args, **kwargs)
        self.fields['proxy'].queryset = Proxy.objects.filter(credential=None)

        if self.instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['password'].widget.attrs['readonly'] = True
            if self.instance.proxy:
                self.fields['proxy'].queryset |= Proxy.objects.filter(pk=self.instance.proxy.pk)

        self.helper = FormHelper()
        if self.instance.pk and self.instance.state == CREDENTIAL_STATE.hold:
            button_holder = ButtonHolder(
                Submit('submit', 'Activate', css_class="btn-success pull-left"),
                Submit('submit', 'Submit', css_class="pull-right")
            )
        else:
            button_holder = ButtonHolder(
                Submit('submit', 'Submit', css_class="pull-right")
            )
        if self.instance.captcha_image:
            self.helper.layout = Layout(
                Div(HTML('<img src="{}" />'.format(self.instance.captcha_image)), css_class='form-group'),
                Div(BasicBootstrapFormField('proxy'), css_class='form-group'),
                Div(BasicBootstrapFormField('email'), css_class='form-group'),
                Div(BasicBootstrapFormField('password'), css_class='form-group'),
                Field('has_linkedin', template='field_layouts/adminlite/checkbox.html'),
                button_holder,
            )
        else:
            self.helper.layout = Layout(
                Div(BasicBootstrapFormField('proxy'), css_class='form-group'),
                Div(BasicBootstrapFormField('email'), css_class='form-group'),
                Div(BasicBootstrapFormField('password'), css_class='form-group'),
                Field('has_linkedin', template='field_layouts/adminlite/checkbox.html'),
                button_holder,
            )
    
    def clean_proxy(self, *args, **kwargs):
        proxy = self.cleaned_data['proxy']
        # Should validate proxy here.
        pass
        return proxy
    
    def save(self, commit=True):
        if self.clean_proxy() is None:
            self.instance.state = CREDENTIAL_STATE.no_proxy
        elif self.instance.state == CREDENTIAL_STATE.no_proxy:
            self.instance.state = CREDENTIAL_STATE.hold
        
        credential = super(CredentialForm, self).save(commit)
        if self.data['submit'] == 'Activate':
            logger.debug("About to activate a credential {}!".format(self.instance))
            self.instance.state = CREDENTIAL_STATE.processing
            recovery_credential.delay(credential.pk)
        return credential