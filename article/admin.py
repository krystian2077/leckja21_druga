from django.contrib import admin
from .models import Article, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'pub_date', 'is_published']
    list_filter = ['is_published', 'category', 'tags', 'pub_date']
    search_fields = ['title', 'content']
    filter_horizontal = ['tags']
    date_hierarchy = 'pub_date'
