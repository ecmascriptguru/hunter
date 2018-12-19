from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Div
from .models import TargetFile, Target
from ...core.widgets.fields import BasicBootstrapFormField


class TargetUploadForm(forms.ModelForm):
    class Meta:
        model = TargetFile
        exclude = ('created_by', )
    
    def __init__(self, *args, **kwargs):
        super(TargetUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            BasicBootstrapFormField('file'),
            BasicBootstrapFormField('encode_type'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-primary pull-right'),
                wrapper_class='form-group',
            ),
        )
    
    def clean_file(self, *args, **kwargs):
        file = self.cleaned_data['file']
        return file