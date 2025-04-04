from rest_framework import serializers

from apps.projects.models import ServiceOption
from apps.projects.serializers import (ServiceOptionSerializer,
                                       ProjectSerializer)
from apps.users.serializers import ProfileSerializer
from .models import Order


class OrderCreateSerializer(serializers.ModelSerializer):
    selected_options = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ServiceOption.objects.all(),
        required=False
    )

    class Meta:
        model = Order
        fields = ['service',
                  'selected_options',
                  'title',
                  'description',
                  'status']
        extra_kwargs = {'status': {'read_only': True}}

    def create(self, validated_data):
        selected_options = validated_data.pop('selected_options', [])
        order = Order.objects.create(**validated_data)
        order.selected_options.set(selected_options)  # Устанавливаем опции
        order.save()  # Вызовет calculate_prices() автоматически
        return order


class OrderListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка заказов"""
    user = ProfileSerializer(read_only=True)
    service = ProjectSerializer(read_only=True)
    selected_options = ServiceOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'title',
            'user',
            'service',
            'selected_options',
            'status',
            'total_price',
            'created_at'
        ]


class OrderDetailSerializer(OrderListSerializer):
    """Сериализатор для детального просмотра заказа"""

    class Meta(OrderListSerializer.Meta):
        fields = OrderListSerializer.Meta.fields + [
            'description',
            'base_price',
            'options_price',
            'updated_at'
        ]


class OrderUpdateSerializer(serializers.ModelSerializer):
    selected_options = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ServiceOption.objects.all(),
        required=False
    )

    class Meta:
        model = Order
        fields = ['title', 'description', 'selected_options', 'status']

    def update(self, instance, validated_data):
        selected_options = validated_data.pop('selected_options', None)

        if selected_options is not None:
            instance.selected_options.set(selected_options)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()  # Автоматический пересчет цен
        return instance


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        extra_kwargs = {
            'status': {'required': True}
        }
