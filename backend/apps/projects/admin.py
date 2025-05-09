from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .models import MediaFile, Category, Project, ServiceOption


class MediaFileInline(GenericStackedInline):
    model = MediaFile
    extra = 1
    fields = ('file', 'media_type', 'order', 'created_at')


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'content_object', 'media_type', 'file', 'order', 'created_at')
    list_filter = ('media_type', 'created_at')
    search_fields = ('file',)
    list_editable = ('order',)
    readonly_fields = ('content_type', 'object_id', 'created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)
    list_per_page = 20


class ServiceOptionInline(admin.StackedInline):
    model = ServiceOption
    extra = 1
    fields = ('title', 'description', 'price', 'deadline_days')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'type', 'title', 'category', 'price', 'deadline_days', 'url', 'user')
    list_filter = ('type', 'category')
    search_fields = ('title', 'description')
    list_editable = ('price', 'deadline_days')
    readonly_fields = ('id',)
    inlines = [MediaFileInline, ServiceOptionInline]
    fieldsets = (
        (None, {
            'fields': ('type', 'title', 'description', 'category', 'user')
        }),
        ('Детали', {
            'fields': ('price', 'deadline_days', 'url')
        }),
    )


@admin.register(ServiceOption)
class ServiceOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'title', 'price', 'deadline_days')
    list_filter = ('project',)
    search_fields = ('title', 'description')
    list_select_related = ('project',)
    raw_id_fields = ('project',)
