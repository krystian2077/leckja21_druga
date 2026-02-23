from django.db import models
from django.utils import timezone
from datetime import timedelta


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True,
                                 blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def is_new(self):
        return timezone.now() - self.pub_date <= timedelta(days=3)
