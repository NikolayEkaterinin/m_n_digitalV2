from django.urls import include, path
from rest_framework import routers
from .views import UserProfileViewSet, UserRegistrationViewSet

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'users', UserProfileViewSet, basename='users')
router.register(r'auth', UserRegistrationViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]