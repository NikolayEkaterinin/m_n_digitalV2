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
    model = Order
    template_name = 'pages/profile.html'
    context_object_name = 'orders'

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
            'profile_user': profile_user,
            'is_own_profile': profile_user == self.request.user,
            'user': self.request.user  # Текущий авторизованный пользователь
        })
        print(f"Context user: {context['profile_user'].id}")  # Debug
        return context