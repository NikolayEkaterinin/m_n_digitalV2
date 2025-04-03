from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch
from apps.users.models import CustomUser
from apps.projects.models import Project, ServiceOption
from .models import Order
from .serializers import (
    OrderCreateSerializer,
    OrderListSerializer,
    OrderDetailSerializer,
    OrderUpdateSerializer,
    OrderStatusSerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с заказами:
    - Создание, просмотр, обновление, удаление заказов
    - Дополнительные экшены для смены статуса
    """
    queryset = Order.objects.none()  # По умолчанию пустой queryset

    def get_queryset(self):
        """Оптимизированный queryset с учетом прав доступа"""
        queryset = Order.objects.select_related(
            'user',
            'service'
        ).prefetch_related(
            Prefetch(
                'selected_options',
                queryset=ServiceOption.objects.select_related('project')
            )
        ).order_by('-created_at')

        # Для администраторов - все заказы
        if self.request.user.is_staff:
            return queryset

        # Для обычных пользователей - только свои заказы
        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'list':
            return OrderListSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        elif self.action == 'change_status':
            return OrderStatusSerializer
        return OrderListSerializer

    def get_permissions(self):
        """Настройка прав доступа"""
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy',
                           'change_status']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """Автоматическое назначение пользователя при создании"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Кастомный экшен для изменения статуса"""
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data['status']
        old_status = order.status

        # Дополнительные проверки перехода статусов
        if old_status == Order.STATUS_COMPLETED and new_status != Order.STATUS_COMPLETED:
            return Response(
                {'error': 'Завершенный заказ нельзя изменить'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """Список заказов текущего пользователя"""
        queryset = self.filter_queryset(
            self.get_queryset().filter(user=request.user)
        )
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['get'])
    def invoice(self, request, pk=None):
        """Генерация счета для заказа (пример кастомного экшена)"""
        order = self.get_object()
        # Здесь может быть логика генерации PDF или других форматов
        return Response({
            'order_id': order.id,
            'total': order.total_price,
            'items': [
                         {'name': order.service.title,
                          'price': order.base_price}
                     ] + [
                         {'name': opt.title, 'price': opt.price}
                         for opt in order.selected_options.all()
                     ]
        })