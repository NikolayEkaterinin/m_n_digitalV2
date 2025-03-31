from django.urls import include, path
from rest_framework import routers
from .views import (UserProfileViewSet,
                    UserRegistrationViewSet,
                    ListProfileViewSet)

router = routers.DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'auth', UserRegistrationViewSet, basename='auth')
router.register(r'list', ListProfileViewSet, basename='list')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),  # Стандартные эндпоинты Djoser
    path('auth/', include('djoser.urls.authtoken')),
]