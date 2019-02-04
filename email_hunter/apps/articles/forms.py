from django import forms
from django_fsm import FSMField
from crispy_forms.layout import Layout, Div, Submit, ButtonHolder, Field
from crispy_forms.helper import FormHelper
from django.core.exceptions import ValidationError
from ...core.widgets.fields import BasicBootstrapFormField
from ...core.utils.parsers import parse_urls
from ..targets import ENCODE_TYPE
from .models import Article, ARTICLE_STATE


class ArticleUploadForm(forms.Form):
    ENCODE_TYPE_CHOICES = (
        (ENCODE_TYPE.unicode, 'UTF-8'),
        (ENCODE_TYPE.latin1, 'Latin'),
        (ENCODE_TYPE.cp1252, 'CP 1252'),
    )

    file = forms.FileField()
    encode_type = forms.ChoiceField(choices=ENCODE_TYPE_CHOICES)
    rows = []

    def __init__(self, *args, **kwargs):
        super(ArticleUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            BasicBootstrapFormField('file'),
            BasicBootstrapFormField('encode_type'),
            ButtonHolder(
                Submit('submit', 'Upload')
            )
        )

    def clean_file(self):
        file = self.cleaned_data['file']
        _, msg, rows = parse_urls(file, encoding=self.data['encode_type'])
        for row in rows:
            if not Article.objects.filter(url=row.get('url')).exists():
                self.rows.append(Article(url=row.get('url'), authors=[]))
            else:
                continue
        
        if len(self.rows) == 0:
            raise ValidationError('This File doesn\'t have any new URL.')
        return file