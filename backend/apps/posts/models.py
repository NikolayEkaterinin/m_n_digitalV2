from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.projects.models import Category, MediaFile
from apps.users.models import CustomUser





class Post(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    category = models.ForeignKey(
        Category,
        related_name='posts',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория поста'
    )

    # Правильное объявление GenericRelation
    media_files = GenericRelation(
        MediaFile,
        related_query_name='post',
        verbose_name='Медиафайлы'
    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title