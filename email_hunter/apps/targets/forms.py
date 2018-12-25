import tldextract
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Div
from ...core.widgets.fields import BasicBootstrapFormField
from ...core.utils.parsers import parse_target
from .models import TargetFile, Target, TARGET_STATE
from .tasks import validate_targets


class TargetUploadForm(forms.ModelForm):
    file = forms.FileField(help_text='Choose a targets file.')

    class Meta:
        model = TargetFile
        exclude = ('created_by', 'filename', )
    
    def __init__(self, *args, **kwargs):
        if kwargs.get('user', None):
            self.user = kwargs.pop('user')

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
        _, msg, rows = parse_target(file, self.cleaned_data['encode_type'])
        if not _:
            if not self.errors['file']:
                self.errors['file'] = list()
            self.errors['file'].append(msg)
        else:
            targets = list()
            for row in rows:
                extract = tldextract.extract(row.pop("url"))
                if extract.suffix == "":
                    continue

                first_name=row.get("first_name", "")
                last_name=row.get("last_name", "")
                domain = "{}.{}".format(extract.domain, extract.suffix)

                if Target.objects.filter(first_name=first_name, 
                    last_name=last_name, domain=domain).exists():
                    continue
                else:
                    row['domain'] = domain
                    row.pop('Index')
                    targets.append(row)
            
            if len(targets) == 0:
                if not self.errors.get('file', None):
                    self.errors['file'] = list()
                self.errors['file'].append('This file doesn\'t have any new target. Choose another file...')
            else:
                self.cleaned_data['new_targets'] = targets
                self.instance.filename = file.name
                self.instance.created_by = self.user
        return file
    
    def save(self, commit=True):
        new_targets = self.cleaned_data.pop('new_targets')
        target_file = super(TargetUploadForm, self).save(commit)
        batch = (Target(**target, created_by=self.user, file=target_file) for target in new_targets)
        target_file.targets.bulk_create(batch)
        return target_file


class TargetUpdateForm(forms.ModelForm):
    class Meta:
        model = Target
        exclude = ('file', 'job', 'created_by', 'state', )
    
    def __init__(self, *args, **kwargs):
        super(TargetUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        if self.instance.state in [TARGET_STATE.to_do, TARGET_STATE.has_error]:
            self.helper.layout = Layout(
                BasicBootstrapFormField('first_name'),
                BasicBootstrapFormField('last_name'),
                BasicBootstrapFormField('domain'),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='btn btn-primary pull-right'),
                    Submit('submit', 'Validate', css_class='btn btn-info pull-left'),
                    wrapper_class='form-group',
                ),
            )
        else:
            self.helper.layout = Layout(
                BasicBootstrapFormField('first_name'),
                BasicBootstrapFormField('last_name'),
                BasicBootstrapFormField('domain'),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='btn btn-primary pull-right'),
                    wrapper_class='form-group',
                ),
            )
    
    def save(self, commit=True):
        if self.data['submit'] == 'Validate':
            task = validate_targets.delay([self.instance.pk])
            self.instance.state = TARGET_STATE.in_progress
        return super(TargetUpdateForm, self).save(commit)