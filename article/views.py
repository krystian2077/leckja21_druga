from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from article.models import Article, Category


@login_required
def profile_view(request):
    """Widok profilu użytkownika"""
    context = {
        'user': request.user,
    }
    return render(request, 'account/profile.html', context)


def article_list_view(request):
    search_query = request.GET.get('q', '')
    sort_order = request.GET.get('sort', 'newest')  # domyślnie: od najnowszych

    # Filtrowanie tylko opublikowanych artykułów z optymalizacją zapytań
    all_articles = (Article.objects.filter(is_published=True).
                    select_related('category').prefetch_related('tags'))

    if search_query:
        # Wyszukiwanie w tytule lub treści
        all_articles = all_articles.filter(
            Q(title__icontains=search_query) | Q(
                content__icontains=search_query)
        )

    # Sortowanie według wybranej opcji
    if sort_order == 'oldest':
        all_articles = all_articles.order_by('pub_date')  # od najstarszych
    else:
        all_articles = all_articles.order_by(
            '-pub_date')  # od najnowszych (domyślnie)

    # Paginacja - 5 najnowszych artykułów na stronę
    paginator = Paginator(all_articles, 5)
    page_number = request.GET.get('page')
    articles_page = paginator.get_page(page_number)

    context = {
        'articles': articles_page,
        'search_query': search_query,
        'sort_order': sort_order,
        'page_obj': articles_page,
    }

    return render(request, 'articles/article_list.html', context)


def category_list_view(request):
    all_categories = Category.objects.all()

    context = {
        'categories': all_categories,
    }

    return render(request, 'categories/category_list.html', context)


def category_detail_view(request, category_id):
    category = Category.objects.get(id=category_id)
    # Filtrowanie artykułów należących do danej kategorii
    articles_in_category = Article.objects.filter(
        category_id=category_id).order_by('-pub_date')

    context = {
        'category': category,
        'articles': articles_in_category,
    }

    return render(request, 'categories/category_detail.html', context)
