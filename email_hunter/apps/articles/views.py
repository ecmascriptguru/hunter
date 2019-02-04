from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy
from .models import Article, ARTICLE_STATE
from .tables import ArticleTable
from .filters import ArticleFilter
from .forms import ArticleUploadForm


class ArticleListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Article
    filterset_class = ArticleFilter
    table_class = ArticleTable
    template_name = 'articles/article_list_view.html'
    strict = False


class ArticleUploadView(LoginRequiredMixin, generic.FormView):
    form_class = ArticleUploadForm
    template_name = 'articles/article_upload_view.html'
    success_url = reverse_lazy('articles:article_list_view')

    def form_valid(self, form):
        count = Article.objects.bulk_create(form.rows)
        return super().form_valid(form)