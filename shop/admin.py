from adminsortable.admin import SortableAdmin
from django.contrib import admin
from django.core.checks import messages
from django.utils.translation import ngettext
from import_export import resources, fields, widgets
from import_export.admin import ImportExportActionModelAdmin

from shop.import_export.widgets import CategoryWidget
from shop.models import Category, Product


@admin.register(Category)
class CategoryAdmin(SortableAdmin):
    search_fields = ('name',)
    list_display = ('name', 'active', 'create_at', 'update_at')
    list_display_links = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'active')
        }),
        ('SEO Настройки', {
            'classes': ('wide', 'extrapretty',),
            'fields': ('seo_title', 'seo_description', 'slug',),
        }),
    )


class ProductResource(resources.ModelResource):
    name = fields.Field(
        column_name='Название',
        attribute='name',
        widget=widgets.Widget())
    description = fields.Field(
        column_name='Описание',
        attribute='description',
        widget=widgets.Widget())
    price = fields.Field(
        column_name='Цена',
        attribute='price',
        widget=widgets.DecimalWidget())
    available = fields.Field(
        column_name='В наличии',
        attribute='available',
        default=1,
        widget=widgets.BooleanWidget())
    category = fields.Field(
        column_name='Категория',
        attribute='category',
        widget=CategoryWidget(Category, 'name'))
    features = fields.Field(
        column_name='Характеристики',
        attribute='features',
        widget=widgets.Widget())

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'price', 'available', 'features')
        export_order = ('id', 'category', 'name', 'price', 'available', 'description', 'features')


@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'category', 'price', 'available', 'create_at', 'update_at')
    list_display_links = ('name',)
    list_filter = ('category',)
    search_fields = ('name',)
    actions = ImportExportActionModelAdmin.actions + ['make_available', 'make_unavailable']
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'description', 'price', 'available', 'image', 'features',)
        }),
        ('SEO Настройки', {
            'classes': ('wide', 'extrapretty',),
            'fields': ('seo_title', 'seo_description'),
        }),
    )

    def make_available(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(request, ngettext(
            '%d товар помечен как "В наличии".',
            '%d товаров помечены как "В наличии".',
            updated,
        ) % updated, messages.SUCCESS)

    make_available.short_description = "Сделать выделенные товары 'В наличии'"

    def make_unavailable(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(request, ngettext(
            '%d товар помечен как "Под заказ".',
            '%d товаров помечены как "Под заказ".',
            updated,
        ) % updated, messages.SUCCESS)

    make_unavailable.short_description = "Сделать выделенные товары 'Под заказ'"
