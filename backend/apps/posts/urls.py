from django.urls import path, include
from rest_framework import routers

from .views import (PostViewSet)

router = routers.DefaultRouter()
router.register(r'', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
]
