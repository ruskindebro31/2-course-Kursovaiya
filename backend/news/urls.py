from django.urls import path
from .views import CategoryListCreateView, ArticleListCreateView, ArticleDetailView, article_comments

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('articles/', ArticleListCreateView.as_view(), name='article-list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('articles/<int:article_id>/comments/', article_comments, name='article-comments'),
]
