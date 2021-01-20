from django.db import models
from solo.models import SingletonModel


class Settings(SingletonModel):
    site_name = models.CharField(max_length=255, verbose_name='Название сайта', default='Банщик')
    site_description = models.CharField(max_length=255, verbose_name='Описание сайта',
                                        default='Банщик всё для бань и саун!')
    phone = models.CharField(max_length=255, verbose_name='Телефон', default='+79991112233')
    address = models.TextField(verbose_name='Адрес', blank=True, default='')
    maintenance_mode = models.BooleanField(verbose_name='Режим обслуживания', default=False)

    def __str__(self):
        return "Настройки сайта"

    class Meta:
        verbose_name = "Настройки"
