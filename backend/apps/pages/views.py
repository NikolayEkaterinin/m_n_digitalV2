from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (CreateView,
                                  ListView,
                                  DetailView,
                                  TemplateView)

from apps.orders.models import Order
from apps.projects.models import Project, Category
from apps.users.models import CustomUser


class IndexListView(TemplateView):
    template_name = 'pages/index.html'

    def get_projects(self):
        return Project.objects.order_by('?')[:6]

    def get_category(self):
        return Category.objects.order_by('?')[:7]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {'projects': self.get_projects(),
             'category': self.get_category()})
        return context
