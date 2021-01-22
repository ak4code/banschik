from django.contrib import admin
from genericadmin.admin import TabularInlineWithGeneric, GenericAdminModelAdmin
from solo.admin import SingletonModelAdmin
from .models import Settings, Page, MenuItem, Menu
from adminsortable.admin import SortableAdmin, SortableTabularInline


@admin.register(Settings)
class SettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Основные', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('site_name', 'site_description', 'phone', 'email', 'address', 'maintenance_mode', 'home')
        }),
        ('SEO Настройки', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('seo_title', 'seo_description'),
        }),
    )

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at', 'update_at')
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ('Основные', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('title', 'content',)
        }),
        ('SEO Настройки', {
            'classes': ('wide', 'extrapretty'),
            'fields': ('seo_title', 'seo_description', 'slug'),
        }),
    )

class MenuItemInlines(TabularInlineWithGeneric, SortableTabularInline):
    extra = 0
    model = MenuItem


@admin.register(Menu)
class MenuAdmin(GenericAdminModelAdmin, SortableAdmin):
    inlines = (MenuItemInlines,)
    content_type_whitelist = ('cms/page', 'shop/category')


try:
    config = Settings.get_solo()
except:
    print('No init base settings')