from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),

    # Дополнительные кастомные URL (если нужны отдельные пути)
    path('orders/my-orders/', OrderViewSet.as_view({'get': 'my_orders'}),
         name='my-orders'),
]