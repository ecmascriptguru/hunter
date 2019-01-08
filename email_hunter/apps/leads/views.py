from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin
from django_filters.views import FilterView
from .models import Lead
from .tables import LeadTable
from .filters import LeadFilter


class LeadListView(LoginRequiredMixin, SingleTableMixin, ExportMixin, FilterView):
    model = Lead
    template_name = 'leads/lead_list_view.html'
    table_class = LeadTable
    filterset_class = LeadFilter
    strict = False