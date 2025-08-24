from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from apps.pages.views import GeneralListView
from .models import Project


class ProjectListView(GeneralListView):
    """Список всех проектов"""
    template_name = 'pages/service.html'
    project_type = Project.PROJECT
    project_limit = None
    category_limit = None
    random_order = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Наши проекты'
        context['type'] = 'project'
        return context


class ServiceListView(GeneralListView):
    """Список всех услуг"""
    template_name = 'pages/service.html'
    project_type = Project.SERVICE
    project_limit = None
    category_limit = None
    random_order = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Наши услуги'
        context['type'] = 'service'
        return context


class ProjectDetailView(DetailView):
    """Детальный просмотр проекта/услуги"""
    model = Project
    template_name = 'includes/detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_options'] = self.object.options.all()
        return context
