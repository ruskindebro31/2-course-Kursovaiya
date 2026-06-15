import os
import django
from django.conf import settings

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'candels.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Создание суперпользователя
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin12345'
    )
    print("Суперпользователь 'admin' успешно создан")
else:
    print("Суперпользователь уже существует")
