from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import (CreateView,
                                  TemplateView)

from apps.projects.models import Project, Category
from apps.users.models import CustomUser
from .forms import CustomUserForm


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


class UserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'registration/registrations.html'
    success_url = reverse_lazy('pages:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request,
              self.object)
        return response
