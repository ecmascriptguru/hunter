import django_filters
from django.db import models
from .models import Lead


class LeadFilter(django_filters.FilterSet):
    class Meta:
        model = Lead
        fields = {
            'email': ['icontains'], 
            'target__first_name': ['icontains'],
            'target__last_name': ['icontains'],
            'engine': ['exact'],
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