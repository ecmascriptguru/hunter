from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy
from .models import Article, ARTICLE_STATE, Bucket
from .tables import ArticleTable, BucketTable
from .filters import ArticleFilter, BucketFilter
from .forms import ArticleUploadForm, BucketForm


class BucketListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Bucket
    strict = False
    table_class = BucketTable
    filterset_class = BucketFilter
    template_name = 'buckets/bucket_list_view.html'
    ajax_template_name = 'buckets/_bucket_list_table.html'

    def get_queryset(self, *args, **kwargs):
        if self.request.is_ajax():
            self.template_name = self.ajax_template_name
        return super().get_queryset(*args, **kwargs)


class BucketUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Bucket
    template_name = 'buckets/bucket_update_view.html'
    form_class = BucketForm
    success_url = reverse_lazy('articles:bucket_list_view')


class ArticleListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Article
    filterset_class = ArticleFilter
    table_class = ArticleTable
    template_name = 'articles/article_list_view.html'
    strict = False


class ArticleUploadView(LoginRequiredMixin, generic.CreateView):
    model = Bucket
    form_class = ArticleUploadForm
    template_name = 'articles/article_upload_view.html'
    success_url = reverse_lazy('articles:article_list_view')

    def get_form_kwargs(self, *args, **kwargs):
        params = super().get_form_kwargs(*args, **kwargs)
        params['user'] = self.request.user
        return params