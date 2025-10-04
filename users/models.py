from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)

    avatar = models.ImageField(upload_to='avatars', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(max_length=255, **NULLABLE, verbose_name='Телефон')
    country = models.CharField(max_length=255, **NULLABLE, verbose_name='Страна')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
