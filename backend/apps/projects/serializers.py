from rest_framework import serializers

from .models import Project, ServiceOption


class ServiceOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOption
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    options = ServiceOptionSerializer(many=True, read_only=True)

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        return project
