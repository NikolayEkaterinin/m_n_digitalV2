import os.path
import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


CustomUser = get_user_model()


class CustomUserForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Пароль",
        strip=False,
        help_text="Минимум 8 символов, не только цифры"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Подтверждение пароля",
        strip=False
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.image:
            default_avatar = os.path.join('staticfiles', 'img',
                                          'default-avatar.png')
            with open(default_avatar, 'rb') as f:
                file_content = ContentFile(f.read())
                user.image.save('default-avatar.png', file_content, save=False)
        if commit:
            user.save()
            self.save_m2m()

        return user

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'telephone',
                  'password1', 'password2', 'image', 'whatsapp']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'pattern': r'^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,}$',
                'placeholder': 'user@example.com'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'pattern': r'^(\+7|8)\d{10}$',
                'placeholder': '+79991234567',
                'title': 'Формат: +79991234567 или 89991234567'
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'pattern': r'^(\+7|8)\d{10}$',
                'placeholder': '+79991234567'
            })
        }

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if not telephone:
            raise forms.ValidationError("Номер телефона обязателен")

        # Удаляем все нецифровые символы, кроме +
        cleaned_phone = re.sub(r'[^\d+]', '', telephone)

        # Проверяем формат: +7XXXXXXXXXX или 8XXXXXXXXXX (11 цифр)
        if not re.match(r'^(\+7|8)\d{10}$', cleaned_phone):
            raise forms.ValidationError(
                "Введите номер в формате +79991234567 или 89991234567")

        return cleaned_phone

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password1')
        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password1', error)
