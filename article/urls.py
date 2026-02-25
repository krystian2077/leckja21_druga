from django.urls import path
from .views import article_list_view, category_list_view, category_detail_view

urlpatterns = [
    path('', article_list_view, name='article_list'),
    path('categories/', category_list_view, name='category-list'),
    path('categories/<int:category_id>/', category_detail_view, name='category-detail'),
]

