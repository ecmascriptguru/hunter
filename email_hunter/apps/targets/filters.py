import django_filters
from django.db import models
from .models import Target


class TargetFilter(django_filters.FilterSet):
    class Meta:
        model = Target
        fields = {
            'first_name': ['icontains'], 
            'last_name': ['icontains'], 
            'domain': ['icontains'],
            'state': ['exact'],
            'file': ['exact'],
            'created_by': ['exact'],
        }
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
         }