from django import forms
from crispy_forms.layout import Layout, Submit, ButtonHolder, Field, Fieldset
from crispy_forms.helper import FormHelper
from .models import Credential
from ...core.widgets.fields import BasicBootstrapFormField


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
        exclude = ('recovery_email', 'recovery_phone')
    
    def __init__(self, *args, **kwargs):
        super(CredentialForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            BasicBootstrapFormField('proxy'),
            BasicBootstrapFormField('email'),
            BasicBootstrapFormField('password'),
            Field('has_linkedin', template='field_layouts/adminlite/checkbox.html'),
            BasicBootstrapFormField('state'),
        )