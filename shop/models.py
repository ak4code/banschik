from adminsortable.models import SortableMixin
from django.core.cache import cache
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from tinymce import HTMLField
from uuslug import uuslug
from cms.models import SEOBase


class Category(SEOBase, SortableMixin):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = HTMLField(blank=True, null=True, verbose_name='Описание')
    slug = models.SlugField(max_length=200, verbose_name='Слаг', blank=True, db_index=True)
    position = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    active = models.BooleanField(default=True, verbose_name='Активно', help_text='Отображение на сайте вкл/выкл')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category', args=[str(self.slug)])

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        if not self.seo_title:
            self.seo_title = self.name
        if not self.seo_description:
            self.seo_description = strip_tags(self.description)[:200]
        cached_categories = cache.get('categories')
        if cached_categories is not None:
            cache.delete('categories')
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['position']


class Product(SEOBase):
    name = models.CharField(max_length=255, default='Товар', verbose_name='Название')
    image = models.ImageField(upload_to='shop/products', blank=True, null=True, verbose_name='Загрузка изображения')
    description = HTMLField(blank=True, null=True, verbose_name='Описание')
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE,
                                 verbose_name='Категория')
    price = models.DecimalField(decimal_places=2, max_digits=20, default=1, verbose_name='Цена')
    features = models.TextField(blank=True, null=True, verbose_name='Характеристики')
    available = models.BooleanField(default=True, help_text='При снятой отметки будет отображатся "Под заказ"',
                                    verbose_name='В наличии')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product', kwargs={
            'slug': self.category.slug,
            'pk': self.pk,
        })

    def save(self, *args, **kwargs):
        if not self.seo_title:
            self.seo_title = self.name
        if not self.seo_description:
            self.seo_description = strip_tags(self.description)[:200]
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['create_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
