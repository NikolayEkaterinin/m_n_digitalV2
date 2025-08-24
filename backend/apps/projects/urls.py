from django.urls import path
from .views import (
    ProjectListView, 
    ServiceListView, 
    ProjectDetailView
)

app_name = 'projects'

urlpatterns = [
    path('', ProjectListView.as_view(), name='list'),
    path('services/', ServiceListView.as_view(), name='services'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='detail'),
]
