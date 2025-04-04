from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.users.models import CustomUser
from apps.projects.models import Project, ServiceOption


class Order(models.Model):
    # Основная информация о заказе
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )

    service = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        limit_choices_to={'type': Project.SERVICE},  # Только услуги
        related_name='orders',
        verbose_name='Услуга'
    )

    selected_options = models.ManyToManyField(
        ServiceOption,
        blank=True,
        related_name='orders',
        verbose_name='Выбранные опции'
    )

    title = models.CharField(
        max_length=150,
        verbose_name='Название заказа'
    )

    description = models.TextField(
        verbose_name='Дополнительная информация',
        blank=True
    )

    # Ценовые поля
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Базовая стоимость',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    options_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость опций',
        default=0,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Итоговая стоимость',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )

    # Статусы и даты
    STATUS_DRAFT = 'draft'
    STATUS_PAID = 'paid'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Черновик'),
        (STATUS_PAID, 'Оплачен'),
        (STATUS_IN_PROGRESS, 'В работе'),
        (STATUS_COMPLETED, 'Завершен'),
        (STATUS_CANCELLED, 'Отменен'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        verbose_name='Статус'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    def calculate_prices(self):
        """
        Рассчитывает стоимость заказа на основе базовой цены услуги и выбранных опций.
        Обновляет поля base_price, options_price и total_price.
        """
        # Рассчитываем базовую цену (из связанной услуги)
        self.base_price = self.service.price if self.service else 0

        # Рассчитываем стоимость всех выбранных опций
        self.options_price = sum(
            option.price for option in self.selected_options.all()
        ) if self.selected_options.exists() else 0

        # Итоговая цена - сумма базовой цены и стоимости опций
        self.total_price = self.base_price + self.options_price

        # Сохраняем изменения (если метод вызывается отдельно от save())
        self.save(update_fields=['base_price', 'options_price', 'total_price'])


    def clean(self):
        """Валидация на уровне модели"""
        if self.service and self.service.type != Project.SERVICE:
            raise ValidationError("Заказ можно создать только для услуги")

    def save(self, *args, **kwargs):
        """Переопределение save с валидацией"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ #{self.id}: {self.title}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']