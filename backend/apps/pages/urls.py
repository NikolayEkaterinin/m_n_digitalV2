from django.contrib import admin
from django.urls import path, include

from .views import IndexListView, UserCreateView

app_name = 'pages'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('create/', UserCreateView.as_view(), name='create_user'),
]
