from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect
from django.utils import timezone


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            # Обновляем last_seen
            request.user.last_seen = timezone.now()
            request.user.save(update_fields=['last_seen'])

            # Очищаем кеш статуса
            cache.delete(f'user_{request.user.pk}_online_status')

        return response



