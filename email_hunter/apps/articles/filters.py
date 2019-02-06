import django_filters
from django.db import models
from .models import Article, Bucket


class BucketFilter(django_filters.FilterSet):
    class Meta:
        model = Bucket
        fields = {
            'name': ['icontains'],
            'user': ['exact'],
            'state': ['exact'],
        }


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = {
            'bucket': ['exact'],
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