from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_class = [AllowAny]
        else:
            permission_class = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_class]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

