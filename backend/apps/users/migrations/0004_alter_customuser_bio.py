# Generated by Django 5.1.7 on 2025-04-13 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, help_text='Введите краткое описание своего профиля', null=True, verbose_name='Краткое описание пользователя'),
        ),
    ]
