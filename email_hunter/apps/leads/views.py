from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django_tables2.views import SingleTableMixin
from .models import Lead
from .tables import LeadTable


class LeadListView(LoginRequiredMixin, SingleTableMixin, generic.ListView):
    model = Lead
    template_name = 'leads/lead_list_view.html'
    table_class = LeadTable