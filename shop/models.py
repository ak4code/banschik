from adminsortable.models import SortableMixin
from django.db import models
from uuslug import uuslug
from cms.models import SEOBase


class Category(SEOBase, SortableMixin):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=200, verbose_name='Слаг', blank=True, db_index=True)
    position = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    active = models.BooleanField(default=True, verbose_name='Активно', help_text='Отображение на сайте вкл/выкл')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['position']
