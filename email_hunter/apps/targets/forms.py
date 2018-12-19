import tldextract
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Div
from .models import TargetFile, Target
from ...core.widgets.fields import BasicBootstrapFormField
from ...core.utils.parsers import parse_target


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
        _, rows = parse_target(file, self.cleaned_data['encode_type'])
        if not _:
            if not self.errors['file']:
                self.errors['file'] = list()
            self.errors['file'].append('Input file not in correct format, must be xls, xlsx, csv, csv.gz, pkl')
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
                self.cleaned_data['filename'] = file.name
        return file
    
    def save(self, commit=True):
        new_targets = self.cleaned_data.pop('new_targets')
        batch = (Target(**target, created_by=self.user) for target in new_targets)
        target_file = super(TargetUploadForm, self).save(commit)
        target_file.targets.bulk_create(batch)
        return target_file