from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'DRAFT'
        PUBLISHED = 'PB', 'PUBLISHED'

    title = models.CharField(max_length=128, verbose_name='Название')
    slug = models.SlugField(max_length=128, blank=False, unique_for_date='published', verbose_name="Слаг")
    content = models.TextField(verbose_name="Контент")
    published = models.DateTimeField(default=timezone.now, verbose_name='Опубликовано')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name='Статус')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Автор')

    objects = models.Manager()
    publish = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.published.year, self.published.month, self.published.day, self.slug])

    class Meta:
        ordering = ['-published']
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        indexes = [models.Index(fields=['-published'])]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering =['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"Comment {self.name} on {self.post}"