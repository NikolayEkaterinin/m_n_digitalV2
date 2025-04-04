from django.contrib.contenttypes.fields import (GenericRelation,
                                                GenericForeignKey)
from django.contrib.contenttypes.models import ContentType
from django.core.validators import URLValidator
from django.db import models


class MediaFile(models.Model):
    MEDIA_TYPES = (
        ('photo', 'Фото'),
        ('video', 'Видео'),
        ('gif', 'GIF'),
    )

    # Поля для GenericForeignKey
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type', 'object_id')

    file = models.FileField(upload_to='media/%Y/%m/%d/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Медиафайл'
        verbose_name_plural = 'Медиафайлы'

    def __str__(self):
        return f"{self.get_media_type_display()} (ID: {self.id})"


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Название категории',
    )
    description = models.TextField()

    class Meta:
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'


class Project(models.Model):
    PROJECT = 'project'
    SERVICE = 'service'
    TYPE_CHOICES = [
        (PROJECT, 'Проект'),
        (SERVICE, 'Услуга'),
    ]

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=PROJECT,
        verbose_name='Тип'
    )
    title = models.CharField(
        max_length=150,
        verbose_name='Название',
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    media_files = GenericRelation(
        MediaFile,
        related_query_name='project',
        verbose_name='Медиафайлы'
    )
    url = models.URLField(
        verbose_name='Ссылка на проект',
        validators=[URLValidator(['http', 'https', ])],
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость работы'
    )
    deadline_days = models.PositiveIntegerField(
        verbose_name='Срок выполнения (в днях)',
        help_text="Количество дней на выполнение работы",
        default=0,
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        Category,
        related_name='project',
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"

    class Meta:
        verbose_name = 'Проект/Услуга'
        verbose_name_plural = 'Проекты/Услуги'


class ServiceOption(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name='Услуга'
    )
    title = models.CharField(
        max_length=150,
        verbose_name='Название опции'
    )
    description = models.TextField(
        verbose_name='Описание опции',
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость опции'
    )
    deadline_days = models.PositiveIntegerField(
        verbose_name='Срок выполнения (в днях)',
        help_text="Количество дней на выполнение работы",
        default=0,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.title} ({self.price})"

    class Meta:
        verbose_name = 'Опция услуги'
        verbose_name_plural = 'Опции услуг'
