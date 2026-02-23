"""
Użycie: python manage.py seed_blog
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import models
from faker import Faker
import random

from article.models import Article, Category, Tag


class Command(BaseCommand):
    help = 'Usuwa wszystkie posty i kategorie, tworzy predefiniowane kategorie i generuje 100 losowych postów'

    def handle(self, *args, **options):
        fake = Faker('pl_PL')

        self.stdout.write(self.style.WARNING('=' * 70))
        self.stdout.write(self.style.WARNING('SEED BLOG - Generowanie danych testowych'))
        self.stdout.write(self.style.WARNING('=' * 70))
        self.stdout.write('')

        # Usunięcie wszystkich istniejących postów i kategorii
        self.stdout.write(self.style.WARNING('Krok 1: Usuwanie istniejących danych...'))

        articles_count = Article.objects.count()
        categories_count = Category.objects.count()
        tags_count = Tag.objects.count()

        Article.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(f'  [OK] Usunieto {articles_count} artykulow'))
        self.stdout.write(self.style.SUCCESS(f'  [OK] Usunieto {categories_count} kategorii'))
        self.stdout.write(self.style.SUCCESS(f'  [OK] Usunieto {tags_count} tagow'))
        self.stdout.write('')

        # Tworzenie kategorii
        self.stdout.write(self.style.WARNING('Krok 2: Tworzenie kategorii...'))

        predefined_categories = [
            'Technologia',
            'Podroze',
            'Kulinaria',
            'Sport',
            'Kultura',
            'Nauka',
            'Biznes',
            'Zdrowie',
            'Motoryzacja',
            'Lifestyle'
        ]

        categories = []
        for cat_name in predefined_categories:
            category = Category.objects.create(name=cat_name)
            categories.append(category)
            self.stdout.write(self.style.SUCCESS(f'  [OK] Utworzono kategorie: {cat_name}'))

        self.stdout.write(self.style.SUCCESS(f'\nLacznie utworzono {len(categories)} kategorii'))
        self.stdout.write('')

        # Krok 3: Tworzenie tagów
        self.stdout.write(self.style.WARNING('Krok 3: Tworzenie tagow...'))

        predefined_tags = [
            'Python', 'Django', 'JavaScript', 'React', 'AI', 'Machine Learning',
            'Tutorial', 'Poradnik', 'Nowosci', 'Recenzja', 'Opinia', 'Analiza',
            'Tips', 'Tricks', 'Best Practices', 'Beginner', 'Advanced', 'Expert',
            'News', 'Update', 'Release', 'Feature', 'Bug Fix', 'Performance',
            'Security', 'Database', 'Frontend', 'Backend', 'Full Stack', 'DevOps'
        ]

        tags = []
        for tag_name in predefined_tags:
            tag = Tag.objects.create(name=tag_name)
            tags.append(tag)

        self.stdout.write(self.style.SUCCESS(f'  [OK] Utworzono {len(tags)} tagow'))
        self.stdout.write('')

        # Krok 4: Tworzenie 100 losowych postów
        self.stdout.write(self.style.WARNING('Krok 4: Generowanie 100 losowych artykułów...'))

        articles_created = 0

        for i in range(100):
            # Losowe dane artykułu
            title = fake.sentence(nb_words=6).rstrip('.')

            # Generowanie treści
            num_paragraphs = random.randint(3, 8)
            content_paragraphs = [fake.paragraph(nb_sentences=random.randint(3, 6))
                                 for _ in range(num_paragraphs)]
            content = '\n\n'.join(content_paragraphs)

            # Losowa kategoria
            category = random.choice(categories)

            #  losowa data z ostatnich 85 dni (grudzień 2025 - luty 2026)
            days_ago = random.randint(0, 85)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)

            pub_date = timezone.now() - timezone.timedelta(
                days=days_ago,
                hours=hours_ago,
                minutes=minutes_ago
            )

            # Losowo czy artykuł jest opublikowany
            is_published = random.random() < 0.95

            # Tworzenie artykułu
            article = Article.objects.create(
                title=title,
                content=content,
                category=category,
                pub_date=pub_date,
                is_published=is_published
            )

            # Losowe przypisanie 1-5 tagów do artykułu
            num_tags = random.randint(1, 5)
            article_tags = random.sample(tags, num_tags)
            article.tags.set(article_tags)

            articles_created += 1

            # Wyświetlanie postępu co 10 artykułów
            if (i + 1) % 10 == 0:
                self.stdout.write(f'  -> Utworzono {i + 1}/100 artykulow...')


        self.stdout.write(self.style.SUCCESS(f'\n[OK] Lacznie utworzono {articles_created} artykulow'))
        self.stdout.write('')


        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('PODSUMOWANIE'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS(f'Kategorie: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Tagi: {Tag.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Artykuly: {Article.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Artykuly opublikowane: {Article.objects.filter(is_published=True).count()}'))
        self.stdout.write(self.style.SUCCESS(f'Artykuly nieopublikowane: {Article.objects.filter(is_published=False).count()}'))
        self.stdout.write('')

        self.stdout.write(self.style.WARNING('Artykuly per kategoria:'))
        for category in categories:
            count = category.article_set.count()
            self.stdout.write(f'  * {category.name}: {count} artykulow')

        self.stdout.write('')
        self.stdout.write(self.style.WARNING('Top 10 najpopularniejszych tagow:'))
        popular_tags = Tag.objects.annotate(
            article_count=models.Count('articles')
        ).order_by('-article_count')[:10]

        for tag in popular_tags:
            self.stdout.write(f'  * {tag.name}: {tag.article_count} artykulow')

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('[OK] Baza danych zostala wypelniona danymi testowymi!'))
        self.stdout.write(self.style.SUCCESS('=' * 70))

