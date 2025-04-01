from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import CustomUser
from .serializers import (RegisterSerializer,
                          ProfileSerializer
                          )


class UserRegistrationViewSet(GenericViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.none()  # Фикс для AssertionError

    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileViewSet(GenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

    @action(methods=['get', 'patch'], detail=False)
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class ListProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        if not self.request.user.is_superuser:
            raise PermissionDenied(
                "У Вас нет доступа к этой функции")
        return super().get_queryset()
