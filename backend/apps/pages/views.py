from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (CreateView,
                                  TemplateView,
                                  FormView,
                                  ListView)

from apps.orders.models import Order
from apps.projects.models import Project, Category
from apps.users.models import CustomUser
from .forms import CustomUserForm

User = get_user_model()


class GeneralListView(TemplateView):
    """Базовый класс для страниц с общими данными (проекты и категории)"""
    project_model = Project  # Модель проектов
    category_model = Category  # Модель категорий
    project_limit = None  # Лимит проектов (None - без лимита)
    category_limit = None  # Лимит категорий по умолчанию как в оригинальном коде
    project_type = None  # Фильтр по типу (project/service)
    random_order = False  # Случайный порядок для проектов

    def get_projects_queryset(self):
        """QuerySet для проектов/услуг с учетом всех параметров"""
        qs = self.project_model.objects.all()

        if self.project_type:
            qs = qs.filter(type=self.project_type)

        if self.random_order:
            qs = qs.order_by('?')

        if self.project_limit:
            qs = qs[:self.project_limit]

        return qs

    def get_category_queryset(self):
        """QuerySet для категорий"""
        qs = self.category_model.objects.all()

        if self.random_order:
            qs = qs.order_by('?')

        if self.category_limit:
            qs = qs[:self.category_limit]

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'projects': self.get_projects_queryset(),
            'category': self.get_category_queryset(),
            'current_type': self.project_type  # Для использования в шаблоне
        })
        return context


class IndexListView(GeneralListView):
    template_name = 'pages/index.html'
    project_limit = 6
    category_limit = 7
    random_order = True


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
    success_url = reverse_lazy(
        'pages:profile')  # Пока нет профиля переходим на основную страницу

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Выполняем аутентификацию
        user = form.get_user()
        login(self.request, user)

        # Перенаправляем на профиль с ID пользователя
        self.success_url = reverse('pages:profile', kwargs={'pk': user.pk})
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       'Ошибка входа. Проверьте логин и пароль')
        return super().form_invalid(form)


# Profile
class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'pages/profile.html'
    context_object_name = 'orders'

    def get_projects(self):
        return Project.objects.filter(user=self.request.user).order_by('-id')

    def get_ordering(self):
        return Order.objects.filter(user=self.request.user).order_by('-id')

    def get_queryset(self):
        profile_user = self.get_profile_user()
        print(f"Showing profile for user ID: {profile_user.id}")  # Debug
        return Order.objects.filter(user=profile_user)

    def get_profile_user(self):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)
        print(
            f"Requested profile for ID: {pk}, found user: {user.username}")  # Debug
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_profile_user()

        context.update({
            'projects': self.get_projects(),
            'ordering': self.get_ordering(),
            'profile_user': profile_user,
            'is_own_profile': profile_user == self.request.user,
            'user': self.request.user  # Текущий авторизованный пользователь
        })
        print(f"Context user: {context['profile_user'].id}")  # Debug
        return context
