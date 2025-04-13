from django.contrib import admin
from django.urls import path, include
from .views import IndexListView, UserCreateView, UserLoginView, ProfileView

app_name = 'pages'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('create/', UserCreateView.as_view(), name='create_user'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),

]