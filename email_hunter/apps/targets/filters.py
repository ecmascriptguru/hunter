import django_filters
from django.db import models
from .models import Target


class TargetFilter(django_filters.FilterSet):
    class Meta:
        model = Target
        fields = ['first_name', 'last_name', 'domain', 'state', 'created_by']
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