from django.apps import AppConfig


class CustomOrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.customorders'
    verbose_name = 'Персонализированные заказы'
