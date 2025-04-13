from datetime import timedelta

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import FileExtensionValidator
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from config.validators import telegram_regex, phone_regex, vk_regex

# Константы
MAX_LENGTH = 50


def social_media_field(verbose_name=None, help_text=None, validators=None):
    return models.CharField(
        verbose_name=verbose_name,
        max_length=MAX_LENGTH,
        unique=False,  # Убираем принудительную уникальность
        blank=True,  # Разрешаем пустые значения в формах
        null=True,  # Разрешаем NULL в базе данных
        help_text=help_text,
        validators=validators if validators else []
    )


class CustomUser(AbstractUser):
    """Модель пользователя"""
    # Переопределяем стандартные поля для устранения конфликтов
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_groups",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_permissions",
        related_query_name="customuser",
    )
    position = models.CharField(
        max_length=30,
        verbose_name='Должность',
        null=True,
        blank=True,
        default='Пользователь'
    )

    image = models.ImageField(
        verbose_name="Фото профиля",
        upload_to="profile_img/",
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],

        null=True,
        blank=True,
    )

    username = models.CharField(
        _('username'),
        max_length=MAX_LENGTH,
        null=False,
        unique=True,
        db_index=True,
        help_text=_(
            'Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    )

    first_name = models.CharField(
        _('first name'),
        max_length=MAX_LENGTH,
        blank=True
    )

    last_name = models.CharField(
        _('last name'),
        max_length=MAX_LENGTH,
        blank=True
    )

    email = models.EmailField(
        _('email address'),
        unique=True
    )

    telegram = social_media_field(
        verbose_name=_('Telegram'),
        help_text=_('Ваш никнейм в телеграм (начинается с @)'),
        validators=[telegram_regex]
    )

    telephone = social_media_field(
        verbose_name=_('Телефон'),
        help_text=_('Введите ваш номер телефона'),
        validators=[phone_regex]
    )

    vk = social_media_field(
        verbose_name=_('VK'),
        help_text=_('Введите ссылку на ваш профиль VK'),
        validators=[vk_regex]
    )

    ok = social_media_field(
        verbose_name=_('Одноклассники'),
        help_text=_('Введите ссылку на ваш профиль в Одноклассниках')
    )

    whatsapp = social_media_field(
        verbose_name=_('WhatsApp'),
        help_text=_('Укажите номер телефона в WhatsApp'),
        validators=[phone_regex]
    )

    linkedin = social_media_field(
        verbose_name=_('LinkedIn'),
        help_text=_('Введите ссылку на ваш профиль в LinkedIn')
    )
    last_seen = models.DateTimeField(null=True, blank=True)

    @property
    def is_online(self):
        cache_key = f'user_{self.pk}_online_status'
        cached_status = cache.get(cache_key)

        if cached_status is not None:
            return cached_status

        from django.contrib.sessions.models import Session

        # Проверка активных сессий
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        has_active_session = any(
            str(self.pk) == session.get_decoded().get('_auth_user_id', '')
            for session in sessions
        )

        # Проверка времени последней активности
        recently_active = (
                self.last_seen and
                (timezone.now() - self.last_seen) < timedelta(minutes=5)
        )

        online_status = has_active_session and recently_active
        cache.set(cache_key, online_status, 60)  # Кешируем на 1 минуту
        return online_status

    def get_active_sessions(self):
        """Возвращает ключи активных сессий пользователя"""
        from django.contrib.sessions.models import Session
        return [session.session_key for session in Session.objects.filter(
            expire_date__gte=timezone.now()
        ) if str(self.pk) in session.get_decoded().get('_auth_user_id', '')]

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _('Пользователи')
        ordering = ('id',)
        constraints = [
            # Условная уникальность для всех социальных полей
            models.UniqueConstraint(
                fields=['telegram'],
                name='unique_telegram_when_not_null',
                condition=models.Q(telegram__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['telephone'],
                name='unique_telephone_when_not_null',
                condition=models.Q(telephone__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['vk'],
                name='unique_vk_when_not_null',
                condition=models.Q(vk__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['ok'],
                name='unique_ok_when_not_null',
                condition=models.Q(ok__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['whatsapp'],
                name='unique_whatsapp_when_not_null',
                condition=models.Q(whatsapp__isnull=False)
            ),
            models.UniqueConstraint(
                fields=['linkedin'],
                name='unique_linkedin_when_not_null',
                condition=models.Q(linkedin__isnull=False)
            ),
        ]
