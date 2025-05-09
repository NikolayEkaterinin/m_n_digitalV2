from django.contrib import admin
from django.utils.html import format_html
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Настройки отображения списка заказов
    list_display = (
        'id',
        'title',
        'user',
        'service',
        'status_badge',
        'total_price',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'status',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'title',
        'user__username',
        'user__email',
        'service__title',
        'description',
    )

    list_select_related = (
        'user',
        'service',
    )

    list_per_page = 25

    # Настройки формы редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'user',
                'service',
                'title',
                'description',
            )
        }),
        ('Цены', {
            'fields': (
                'base_price',
                'options_price',
                'total_price',
            )
        }),
        ('Статус и даты', {
            'fields': (
                'status',
                'created_at',
                'updated_at',
            )
        }),
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'total_price',
    )

    filter_horizontal = (
        'selected_options',
    )

    # Кастомные методы
    def status_badge(self, obj):
        status_colors = {
            'draft': 'gray',
            'paid': 'green',
            'in_progress': 'blue',
            'completed': 'purple',
            'cancelled': 'red',
        }
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 8px; border-radius: 10px;">{}</span>',
            status_colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )

    status_badge.short_description = 'Статус'

    # Переопределение действий
    actions = [
        'mark_as_paid',
        'mark_as_in_progress',
        'mark_as_completed',
        'mark_as_cancelled',
    ]

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(status=Order.STATUS_PAID)
        self.message_user(request,
                          f"{updated} заказов помечены как оплаченные")

    mark_as_paid.short_description = "Пометить как оплаченные"

    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status=Order.STATUS_IN_PROGRESS)
        self.message_user(request, f"{updated} заказов помечены как в работе")

    mark_as_in_progress.short_description = "Пометить как в работе"

    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status=Order.STATUS_COMPLETED)
        self.message_user(request,
                          f"{updated} заказов помечены как завершенные")

    mark_as_completed.short_description = "Пометить как завершенные"

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status=Order.STATUS_CANCELLED)
        self.message_user(request,
                          f"{updated} заказов помечены как отмененные")

    mark_as_cancelled.short_description = "Пометить как отмененные"

    # Автоматический расчет цен при сохранении
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.calculate_prices()
        obj.save()

    # Автозаполнение пользователя при создании
    def get_changeform_initial_data(self, request):
        return {
            'user': request.user,
        }