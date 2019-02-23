from django import forms
from django.conf import settings
from django_fsm import FSMField
from crispy_forms.layout import Layout, Div, Submit, ButtonHolder, Field
from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError
from ...core.widgets.fields import BasicBootstrapFormField
from ...core.utils.parsers import parse_urls
from ..targets import ENCODE_TYPE
from .models import Article, ARTICLE_STATE, Bucket, BUCKET_STATE
from .tasks import extract_authors


class BucketForm(forms.ModelForm):
    class Meta:
        model = Bucket
        exclude = ('user', 'state', 'is_test_data', 'jobs', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        if self.instance.is_ready:
            self.helper.layout = Layout(
                BasicBootstrapFormField('name'),
                ButtonHolder(
                    Submit('submit', 'Save Changes'),
                    Submit('submit', 'Start Extraction', css_class='pull-right'),
                )
            )
        else:
            self.helper.layout = Layout(
                BasicBootstrapFormField('name'),
                ButtonHolder(
                    Submit('submit', 'Save Changes'),
                )
            )
    
    def clean(self, *args, **kwargs):
        if self.data['submit'] == 'Start Extraction' and not self.instance.is_ready:
            raise ValidationError('This bucket is not ready to get started.\n Please try again later.')
        
        return super().clean(*args, **kwargs)

    def save(self, commit=True):
        if self.data['submit'] == 'Start Extraction':
            ready_articles = self.instance.ready_articles
            ids = [a.id for a in ready_articles]
            ready_articles.update(state=ARTICLE_STATE.pending)
            self.instance.state = BUCKET_STATE.pending
            self.instance.jobs = []
            super().save(commit)
            for i in range(0, len(ids), settings.AUTHOR_EXTRACTION_BATCH_SIZE):
                task = extract_authors.delay(self.instance.pk, ids[i:i + settings.AUTHOR_EXTRACTION_BATCH_SIZE])
                self.instance.jobs.append(task.id)
            # self.instance.job_uuid = extract_authors.delay(self.instance.pk, ids).id
        
        return super().save(commit)


class ArticleUploadForm(forms.ModelForm):
    class Meta:
        model = Bucket
        exclude = ('name', 'user', 'state', 'jobs', )

    ENCODE_TYPE_CHOICES = (
        (ENCODE_TYPE.unicode, 'UTF-8'),
        (ENCODE_TYPE.latin1, 'Latin'),
        (ENCODE_TYPE.cp1252, 'CP 1252'),
    )

    file = forms.FileField()
    encode_type = forms.ChoiceField(choices=ENCODE_TYPE_CHOICES)
    rows = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ArticleUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            BasicBootstrapFormField('file'),
            BasicBootstrapFormField('encode_type'),
            Field('is_test_data', template='field_layouts/adminlite/checkbox.html'),
            ButtonHolder(
                Submit('submit', 'Upload')
            )
        )

    def clean_file(self):
        file = self.cleaned_data['file']
        self.rows = []
        _, msg, rows = parse_urls(file, encoding=self.data['encode_type'],
                is_test_data=self.cleaned_data['is_test_data'])
        
        if not _:
            raise ValidationError(msg)
        else:
            for row in rows:
                if not Article.objects.filter(url=row.get('url')).exists():
                    if self.cleaned_data['is_test_data']:
                        self.rows.append(Article(url=row.get('url'), authors={
                            'origin': ' '.join([str(row.get('first_name')), str(row.get('last_name'))]).strip()
                        }, bucket=self.instance))
                    else:
                        self.rows.append(Article(url=row.get('url'), authors={}, bucket=self.instance))
                else:
                    continue
            
            if len(self.rows) == 0:
                raise ValidationError('This File doesn\'t have any new URL.')
        return file
    
    def save(self, commit=True):
        self.instance.user = self.user
        if not self.instance.pk:
            self.instance.name = self.cleaned_data['file'].name
        
        super().save(commit=commit)

        if len(self.rows) > 0:
            for article in self.rows:
                article.bucket = self.instance
            
            for i in range(0, len(self.rows), 500):
                self.instance.articles.bulk_create(self.rows[i: i + 500])
            # self.instance.articles.bulk_create(self.rows)
        
        return self.instance