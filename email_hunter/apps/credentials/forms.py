from django import forms
from crispy_forms.layout import Layout, Submit, ButtonHolder, Field, Fieldset, Div
from crispy_forms.helper import FormHelper
from .models import Credential, CREDENTIAL_STATE
from ...core.widgets.fields import BasicBootstrapFormField
from ..proxies.models import Proxy


class CredentialUploadForm(forms.Form):
    file = forms.FileField(required=True, help_text='Upload a file including credentials')

    def __init__(self, *args, **kwargs):
        super(CredentialUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_method = 'post'
        self.helper.layout = Layout(
            BasicBootstrapFormField('file'),
            ButtonHolder(Submit('submit', 'Upload', css_class="pull-right"))
        )
    
    def save(self):
        pass


class CredentialForm(forms.ModelForm):
    class Meta:
        model = Credential
        exclude = ('recovery_email', 'recovery_phone', 'state')
    
    def __init__(self, *args, **kwargs):
        super(CredentialForm, self).__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields['proxy'].queryset = Proxy.objects.filter(credential=None)
        else:
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['password'].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(BasicBootstrapFormField('proxy'), css_class='form-group'),
            Div(BasicBootstrapFormField('email'), css_class='form-group'),
            Div(BasicBootstrapFormField('password'), css_class='form-group'),
            Field('has_linkedin', template='field_layouts/adminlite/checkbox.html'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class="pull-right")
            )
        )
    
    def clean_proxy(self, *args, **kwargs):
        proxy = self.cleaned_data['proxy']
        # Should validate proxy here.
        print(proxy)
        return proxy
    
    def save(self, commit=True):
        if self.instance.proxy:
            self.instance.state = CREDENTIAL_STATE.hold
        
        return super(CredentialForm, self).save(commit)