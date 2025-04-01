from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Project, ServiceOption
from .serializers import ProjectSerializer, ServiceOptionSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_permissions(self):
        # Разные permissions для разных действий
        if self.action == 'get_projects':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(methods=['get'], detail=False)
    def get_projects(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ServiceOptionViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceOptionSerializer
    queryset = ServiceOption.objects.all()

    def get_queryset(self):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
