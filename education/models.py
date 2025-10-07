from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Education(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образования'
