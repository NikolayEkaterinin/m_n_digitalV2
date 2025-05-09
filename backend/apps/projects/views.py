from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from apps.pages.views import GeneralListView
from .models import Project, ServiceOption
from .serializers import ProjectSerializer, ServiceOptionSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get_permissions(self):
        # Разные permissions для разных действий
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]


class ServiceOptionViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceOptionSerializer
    queryset = ServiceOption.objects.all()

    def get_queryset(self):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


"""
Далее идут views для отображение на странице услуг и проектов
"""


class ProjectListView(GeneralListView):
    template_name = 'pages/service.html'
    project_type = Project.PROJECT
    project_limit = None
    category_limit = None
    random_order = True


class ServiceListView(GeneralListView):
    template_name = 'pages/service.html'
    project_type = Project.SERVICE
    project_limit = None
    category_limit = None
    random_order = True
