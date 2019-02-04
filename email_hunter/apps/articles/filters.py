import django_filters
from django.db import models
from .models import Article


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = {
            'url': ['icontains'], 
            'state': ['exact'],
        }
        # filter_overrides = {
        #     models.CharField: {
        #         'filter_class': django_filters.CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'icontains',
        #         },
        #     },
        #     models.BooleanField: {
        #         'filter_class': django_filters.BooleanFilter,
        #         'extra': lambda f: {
        #             'widget': forms.CheckboxInput,
        #         },
        #     },
        #  }