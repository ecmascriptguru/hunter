from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from django_tables2.views import SingleTableMixin
from .models import Target
from .forms import TargetUploadForm
from .tables import TargetTable


class TargetListView(SingleTableMixin, generic.ListView):
    decorators = [login_required]
    model = Target
    template_name = 'targets/target_list_view.html'
    table_class = TargetTable


class TargetUploadView(generic.FormView):
    form_class = TargetUploadForm
    template_name = 'targets/target_upload_view.html'