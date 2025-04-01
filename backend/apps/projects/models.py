from django.core.validators import FileExtensionValidator, URLValidator
from django.db import models


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
    image = models.ImageField(
        upload_to="project_img/",
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        verbose_name='Изображение проекта',
        blank=True,
        null=True
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
