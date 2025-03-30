from django.core.validators import RegexValidator

telegram_regex = RegexValidator(
    regex='^@',
    message='Строка должна начинаться с @'
)

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message=f"Номер телефона должен быть в"
            f"формате: '+999999999'. Допустимо до 15 цифр."
)

vk_regex = RegexValidator(
    regex=r'^(https?:\/\/)?(www\.)?vk\.com\/[a-zA-Z0-9_.]{1,}$',
    message='Формат ссылки не соответствует требованиям'
)
