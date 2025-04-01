from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'image',
            'email',
            'telegram',
            'telephone',
            'vk',
            'ok',
            'whatsapp',
            'linkedin',
            'password'
        ]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'image',
            'email',
            'telegram',
            'telephone',
            'vk',
            'ok',
            'whatsapp',
            'linkedin'
        ]
    read_only_fields = ['id']


