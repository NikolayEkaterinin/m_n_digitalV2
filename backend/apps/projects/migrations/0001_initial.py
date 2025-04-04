# Generated by Django 5.1.7 on 2025-04-04 21:40

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название категории')),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': ('Категория',),
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('file', models.FileField(upload_to='media/%Y/%m/%d/')),
                ('media_type', models.CharField(choices=[('photo', 'Фото'), ('video', 'Видео'), ('gif', 'GIF')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Медиафайл',
                'verbose_name_plural': 'Медиафайлы',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('project', 'Проект'), ('service', 'Услуга')], default='project', max_length=10, verbose_name='Тип')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('url', models.URLField(blank=True, null=True, validators=[django.core.validators.URLValidator(['http', 'https'])], verbose_name='Ссылка на проект')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость работы')),
                ('deadline_days', models.PositiveIntegerField(blank=True, default=0, help_text='Количество дней на выполнение работы', null=True, verbose_name='Срок выполнения (в днях)')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project', to='projects.category')),
            ],
            options={
                'verbose_name': 'Проект/Услуга',
                'verbose_name_plural': 'Проекты/Услуги',
            },
        ),
        migrations.CreateModel(
            name='ServiceOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название опции')),
                ('description', models.TextField(blank=True, verbose_name='Описание опции')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость опции')),
                ('deadline_days', models.PositiveIntegerField(blank=True, default=0, help_text='Количество дней на выполнение работы', null=True, verbose_name='Срок выполнения (в днях)')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='projects.project', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Опция услуги',
                'verbose_name_plural': 'Опции услуг',
            },
        ),
    ]
