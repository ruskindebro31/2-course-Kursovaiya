from django.db import models
from django.conf import settings


class Profile(models.Model):
    """Профиль пользователя: био, аватар, контактная информация."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Это будет дефолтный User
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(blank=True, max_length=500, verbose_name='О себе')
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    phone = models.CharField(max_length=15, blank=True, verbose_name='Телефон')
    address = models.TextField(blank=True, max_length=500, verbose_name='Адрес')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"


# Автоматическое создание профиля при регистрации
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Создать профиль при создании пользователя."""
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
