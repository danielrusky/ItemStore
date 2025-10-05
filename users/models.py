from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Имейл')
    phone = models.CharField(max_length=25, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    email_confirmed = models.BooleanField(default=False)
    token = models.CharField(max_length=255, **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
