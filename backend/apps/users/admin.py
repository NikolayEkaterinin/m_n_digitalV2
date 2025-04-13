from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'first_name',
                    'last_name',
                    'email',
                    'telegram',
                    'telephone',
                    'vk',
                    'ok',
                    'whatsapp',
                    'linkedin',
                    'position',
                    )
    search_fields = ('username',
                     'first_name',
                     'last_name',
                     'email',
                     'telegram',
                     'telephone',
                     'vk',
                     'ok',
                     'whatsapp',
                     'linkedin',
                     'position',
                     )
    list_filter = ('username',
                   'first_name',
                   'last_name',
                   'email',
                   'telegram',
                   'telephone',
                   'vk',
                   'ok',
                   'whatsapp',
                   'linkedin',
                   'position',
                   )
