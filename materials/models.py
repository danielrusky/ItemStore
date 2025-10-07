from django.db import models

NULLABLE = {"blank": True, "null": True}


class Material(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название", unique=True)
    slug = models.SlugField(verbose_name="Slug", **NULLABLE)
    content = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(**NULLABLE, verbose_name="Картинка")
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")
    likes_count = models.IntegerField(default=0, verbose_name="количесвто Лайков")
    dislikes_count = models.IntegerField(default=0, verbose_name="количество Дизлайков")
    publicated = models.BooleanField(default=True, verbose_name="Признак публикации")

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ("title",)


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    description = models.TextField(max_length=1000, verbose_name="Описание", **NULLABLE)
    record = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name="Запись")

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("record",)


