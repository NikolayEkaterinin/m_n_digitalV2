# Generated by Django 5.1.7 on 2025-04-13 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_last_seen_customuser_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, help_text='Введите краткое описание своего профиля', null=True, verbose_name='раткое описание пользователя'),
        ),
    ]
