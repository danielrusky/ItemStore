from django.db import models
import datetime

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(verbose_name='Изображение', upload_to='img/', **NULLABLE)
    created_at = models.DateTimeField(verbose_name='Поле_для_дальнейшего_удаления', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(verbose_name='Изображение', upload_to='img/', **NULLABLE)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Цена', **NULLABLE)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_modified = models.DateTimeField(verbose_name='Дата последнего изменения')
    is_active = models.BooleanField(default=True, verbose_name='в наличие')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Contacts(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')
    avatar = models.ImageField(upload_to='contacts/', verbose_name="Картинка", **NULLABLE)

    def __str__(self):
        return f"{self.name}({self.phone})"

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ('phone',)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    v_number = models.IntegerField(default=1)
    v_name = models.CharField(max_length=100, default="changed")
    current = models.BooleanField(default=True)
    add_date = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ("v_name",)
