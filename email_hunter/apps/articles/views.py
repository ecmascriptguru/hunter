from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from .models import Article, ARTICLE_STATE
from .tables import ArticleTable
from .filters import ArticleFilter


class ArticleListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Article
    filterset_class = ArticleFilter
    table_class = ArticleTable
    template_name = 'articles/article_list_view.html'