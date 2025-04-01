from django.urls import path, include
from rest_framework import routers

from .views import (ProjectViewSet)

router = routers.DefaultRouter()
router.register(r'', ProjectViewSet, basename='projects')

urlpatterns = [
    path('', include(router.urls)),
]
