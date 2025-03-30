from django.contrib.auth.models import AbstractUser
from django.db import models

from config.valodators import telegram_regex, phone_regex, vk_regex

# Константы
MAX_LENGTH = 50


def social_media_field(verbose_name=None, help_text=None,
                       validators=None):
    return models.CharField(
        verbose_name=verbose_name,
        max_length=MAX_LENGTH,
        unique=True,
        blank=True,
        null=False,
        help_text=help_text,
        validators=validators
    )


class CustomUser(AbstractUser):
    """Модель пользователя"""
    username = models.CharField(
        max_length=MAX_LENGTH,
        null=False,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True
    )

    first_name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True
    )

    telegram = social_media_field(
        verbose_name='telegram',
        help_text='Ваш никнейм в телеграм',
        validators=[telegram_regex]
    )

    telephone = social_media_field(
        verbose_name='телефон',
        help_text='Введите ваш номер телефона',
        validators=[phone_regex]
    )

    vk = social_media_field(
        verbose_name='vk',
        help_text='Введите ссылку на ваш профиль VK',
        validators=[vk_regex]
    )
    ok = social_media_field(
        verbose_name='ok',
        help_text='Введите ссылку на ваш профиль в Однокласниках'
    )
    whatsapp = social_media_field(
        verbose_name='WhatSap',
        help_text='Укажите номер телефона в WhatSap',
        validators=[phone_regex]
    )
    linkedin = social_media_field(
        verbose_name='LinkedIn',
        help_text='Введите ссылку на ваш профиль в LinkedIn'
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)
