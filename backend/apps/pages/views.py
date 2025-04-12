from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import (CreateView,
                                  TemplateView,
                                  FormView)
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
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


# Create user
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


# Login user
class UserLoginView(FormView):
    template_name = 'registration/authorization.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('pages:index') #Пока нет профиля переходим на основную страницу

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request,
                         f'Добро пожаловать, {user.username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       'Ошибка входа. Проверьте логин и пароль')
        return super().form_invalid(form)
