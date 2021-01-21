from django.conf import settings
from django.db import models
from solo.models import SingletonModel
from django.core.cache import cache
from adminsortable.models import SortableMixin
from tinymce import HTMLField
from uuslug import uuslug
from django.utils.html import strip_tags


class SEOBase(models.Model):
    seo_title = models.CharField(max_length=255, blank=True, null=True, verbose_name='SEO заголовок')
    seo_description = models.TextField(max_length=255, blank=True, null=True, verbose_name='SEO описание')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return f"{self.seo_title}"

    class Meta:
        abstract = True


class Settings(SEOBase, SingletonModel):
    site_name = models.CharField(max_length=255, verbose_name='Название сайта', default='Банщик')
    site_description = models.TextField(verbose_name='Описание сайта', default='Банщик всё для бань и саун!')
    phone = models.CharField(max_length=255, verbose_name='Телефон', default='+79991112233')
    address = models.TextField(verbose_name='Адрес', blank=True, default='')
    maintenance_mode = models.BooleanField(verbose_name='Режим обслуживания', default=False)
    home = models.OneToOneField('Page', verbose_name='Главная страница', blank=True, null=True,
                                on_delete=models.SET_NULL)

    def __str__(self):
        return "Настройки сайта"

    def save(self, *args, **kwargs):
        if not self.seo_title:
            self.seo_title = self.site_name
        if not self.seo_description:
            self.seo_description = strip_tags(self.site_description)[:200]
        super(Settings, self).save(*args, **kwargs)

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


class Page(SEOBase):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = HTMLField(blank=True, default=' ', verbose_name='Контент')
    slug = models.CharField(max_length=255, blank=True, default=' ', verbose_name='ЧПУ ссылка', db_index=True)

    def get_absolute_url(self):
        pass
        # return reverse('core:page', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        if not self.seo_title:
            self.seo_title = self.title
        if not self.seo_description:
            self.seo_description = strip_tags(self.content)[:200]
        super(Page, self).save(*args, **kwargs)

    class Meta:
        ordering = ['create_at']
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
