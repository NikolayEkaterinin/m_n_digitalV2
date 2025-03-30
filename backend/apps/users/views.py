from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import AllowAny

from .models import CustomUser
from .serializers import RegisterSerializer, ProfileSerializer


class UserRegistrationViewSet(ModelViewSet):  # Изменили на GenericViewSet
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @action(methods=['post'], detail=False, url_path='register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_serializer = self.get_serializer(user)
        return Response(response_serializer.data,
                        status=status.HTTP_201_CREATED)


class UserProfileViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'patch', 'head',
                         'options']  # Ограничиваем методы

    def get_object(self):
        return self.request.user  # Всегда работаем с текущим пользователем

    @action(methods=['get', 'patch'], detail=False, url_path='me')
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
