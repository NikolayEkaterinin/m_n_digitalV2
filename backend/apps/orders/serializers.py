from rest_framework import serializers

from apps.projects.models import Project, ServiceOption
from apps.projects.serializers import ServiceOptionSerializer
from apps.users.serializers import ProfileSerializer
from .models import Order


class OrderCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заказа"""
    selected_options = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ServiceOption.objects.all(),
        required=False
    )

    class Meta:
        model = Order
        fields = [
            'service',
            'selected_options',
            'title',
            'description',
            'status'
        ]
        extra_kwargs = {
            'status': {'read_only': True}  # Статус нельзя менять при создании
        }

    def validate_service(self, value):
        """Проверка, что выбранная услуга действительно является услугой"""
        if value.type != Project.SERVICE:
            raise serializers.ValidationError(
                "Можно выбрать только услугу (не проект)")
        return value

    def validate(self, data):
        """Общая валидация данных"""
        service = data.get('service')
        selected_options = data.get('selected_options', [])

        # Проверка, что опции принадлежат выбранной услуге
        if service and selected_options:
            invalid_options = [
                opt for opt in selected_options
                if opt.project_id != service.id
            ]
            if invalid_options:
                raise serializers.ValidationError({
                    'selected_options': f"Опции {[opt.id for opt in invalid_options]} не принадлежат выбранной услуге"
                })

        return data

    def create(self, validated_data):
        """Создание заказа с автоматическим расчетом цен"""
        selected_options = validated_data.pop('selected_options', [])
        order = Order.objects.create(**validated_data)

        if selected_options:
            order.selected_options.set(selected_options)

        # Автоматический расчет цен
        order.base_price = order.service.price
        order.options_price = sum(opt.price for opt in selected_options)
        order.total_price = order.base_price + order.options_price
        order.save()

        return order


class OrderListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка заказов"""
    user = ProfileSerializer(read_only=True)
    service = ProfileSerializer(read_only=True)
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
    """Сериализатор для обновления заказа"""
    selected_options = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ServiceOption.objects.all(),
        required=False
    )

    class Meta:
        model = Order
        fields = [
            'title',
            'description',
            'selected_options',
            'status'
        ]
        extra_kwargs = {
            'status': {'required': False}
        }

    def update(self, instance, validated_data):
        """Обновление заказа с пересчетом цен при изменении опций"""
        selected_options = validated_data.pop('selected_options', None)

        if selected_options is not None:
            instance.selected_options.set(selected_options)
            instance.options_price = sum(opt.price for opt in selected_options)
            instance.total_price = instance.base_price + instance.options_price

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        extra_kwargs = {
            'status': {'required': True}
        }
