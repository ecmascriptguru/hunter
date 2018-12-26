import tldextract
from django import forms
from django.conf import settings
from django.core.validators import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Div, HTML
from ...core.widgets.fields import BasicBootstrapFormField
from ...core.utils.parsers import parse_target
from ...apps.jobs.models import Job, JOB_STATE
from ...apps.credentials.models import Credential
from .models import TargetFile, Target, TARGET_STATE, TARGET_FILE_STATE
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
            self.instance.job = Job.objects.create(internal_uuid=task.id, state=JOB_STATE.pending)
        return super(TargetUpdateForm, self).save(commit)


class TargetFileStartForm(forms.ModelForm):
    class Meta:
        model = TargetFile
        fields = []
    
    def __init__(self, *args, **kwargs):
        super(TargetFileStartForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            ButtonHolder(
                Div(
                    HTML('<h4>Are you sure that you want to start targets in this file?</h4>'),
                    css_class='form-group'
                ),
                Submit('submit', 'Start', css_class='btn btn-primary pull-right'),
                wrapper_class='form-group',
            ),
        )
    
    def clean(self, *args, **kwargs):
        if not self.instance.is_ready:
            raise ValidationError('This file is not ready to get started.')
        if not Credential.is_available():
            raise ValidationError('There is no available credentials now. Please try again.')
        return super(TargetFileStartForm, self).clean(*args, **kwargs)

    def save(self, commit=True):
        limit = 2
        if hasattr(settings, 'EMAIL_HUNTER_BATCH_SIZE'):
            limit = settings.EMAIL_HUNTER_BATCH_SIZE

        todos = self.instance.todos(limit)
        try:
            task = validate_targets.delay([target.pk for target in todos])
            self.instance.state = TARGET_FILE_STATE.pending
            job = Job.objects.create(internal_uuid=task.id, state=JOB_STATE.pending)
            for todo in todos:
                todo.state = TARGET_STATE.pending 
                todo.job = job
                todo.save()
            
            return super(TargetFileStartForm, self).save(commit)
        except Exception as e:
            raise ValidationError(str(e))
            return None