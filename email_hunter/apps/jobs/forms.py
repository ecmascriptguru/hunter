from django import forms
from django_fsm import FSMField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, ButtonHolder, Div,
            Submit, HTML, Button)
from config.celery_app import celery_app            
from .models import Job, JOB_STATE
from ...apps.targets.models import TargetFile, TARGET_FILE_STATE, TARGET_STATE


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [ ]
    
    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        if self.instance.state in [JOB_STATE.pending, JOB_STATE.in_progress]:
            self.helper.layout = Layout(
                HTML('<button class="btn btn-xs btn-default pull-right absolute-right" type="submit" name="submit" value="stop" title="Stop">'
                        '<i class="fa fa-stop"></i>'
                    '</button>')
            )
        else:
            self.helper.layout = Layout(
                HTML('<button class="btn btn-xs btn-danger pull-right absolute-right" type="submit" name="submit" value="archive" title="Archive">'
                        '<i class="fa fa-trash"></i>'
                    '</button>')
            )
    
    def save(self, commit=True):
        if self.data['submit'] == 'stop':
            celery_app.control.revoke(self.instance.internal_uuid, 
                    terminate=True, signal='SIGUSR1')
            
            if self.instance.file is not None and\
                self.instance.file.state in [TARGET_FILE_STATE.pending, TARGET_FILE_STATE.in_progress]:
                self.instance.file.state = TARGET_FILE_STATE.done
                self.instance.file.save()
            
            self.instance.targets.filter(state__in=[TARGET_STATE.pending, TARGET_STATE.in_progress])\
                .update(state=TARGET_STATE.to_do)
            self.instance.state = JOB_STATE.completed
        elif self.data['submit'] == 'archive':
            self.instance.state = JOB_STATE.archived
        return super(JobForm, self).save(commit)