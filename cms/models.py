from django.conf import settings
from django.db import models
from solo.models import SingletonModel
from django.core.cache import cache
from adminsortable.models import SortableMixin


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


class Menu(SortableMixin):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=200, verbose_name='Слаг', unique=True)
    position = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        cached_menus = cache.get(settings.MENU_CACHE_KEY)
        if cached_menus is not None:
            cache.delete(settings.MENU_CACHE_KEY)
        super(Menu, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        ordering = ['position']


class MenuItem(SortableMixin):
    LINK_TARGET_CHOICES = (
        ('_blank', '_blank'),
        ('_top', '_top'),
        ('_parent', '_parent'),
    )
    name = models.CharField(max_length=255, verbose_name='Название')
    url = models.CharField(max_length=255, verbose_name='Ссылка')
    title = models.CharField(max_length=255, verbose_name='Подсказка', blank=True, null=True)
    target = models.CharField(
        max_length=10,
        choices=LINK_TARGET_CHOICES,
        null=True,
        blank=True
    )
    menu = models.ForeignKey('Menu', related_name='items', on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def save(self, *args, **kwargs):
        cached_menus = cache.get(settings.MENU_CACHE_KEY)
        if cached_menus is not None:
            cache.delete(settings.MENU_CACHE_KEY)
        super(MenuItem, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} -> {self.url}'

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'
        ordering = ['position']
