from django.db import models
from django.utils import timezone
from datetime import timedelta


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def is_new(self):
        """Sprawdza czy artykuł został opublikowany w ciągu ostatnich 3 dni."""
        return timezone.now() - self.pub_date <= timedelta(days=3)
