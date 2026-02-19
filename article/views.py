from django.shortcuts import render

from article.models import Article, Category


# Zakomentowane - kod testowy ORM (wykonywał się przy każdym imporcie)
# all_articles = Article.objects.all()
#
# for article in all_articles:
#     print(article.title)
#
#
# new_article = Article.objects.create(
#     title="Nowy artykuł o Django",
#     content="Treść artykułu o potędze ORM."
# )
# print(f"Utworzono artykuł o ID: {new_article.id}")
#
# django_articles = Article.objects.filter(title__contains="Django")
#
# try:
#     specific_article = Article.objects.get(id=1)
#     print(f"Znaleziono artykuł: {specific_article.title}")
#
#     specific_article.title = "Zaktualizowany tytuł"
#     specific_article.save() # Metoda save() zapisuje zmiany w bazie
# except Article.DoesNotExist:
#     print("Artykuł o ID 1 nie istnieje.")


def article_list_view(request):
    search_query = request.GET.get('q', '')

    all_articles = Article.objects.filter(is_published=True)

    if search_query:
        all_articles = all_articles.filter(title__icontains=search_query)

    all_articles = all_articles.order_by('-pub_date')

    context = {
        'articles': all_articles,
        'search_query': search_query,
    }

    return render(request, 'articles/article_list.html', context)


def category_list_view(request):

    all_categories = Category.objects.all()

    context = {
        'categories': all_categories,
    }

    return render(request, 'categories/category_list.html', context)


def category_detail_view(request, category_id):
    """Widok szczegółowy kategorii z listą powiązanych artykułów."""
    category = Category.objects.get(id=category_id)

    context = {
        'category': category,
    }

    return render(request, 'categories/category_detail.html', context)


