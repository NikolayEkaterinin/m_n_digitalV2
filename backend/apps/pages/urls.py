from django.contrib import admin
from django.urls import path, include

from .views import IndexListView

app_name = 'pages'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
]
