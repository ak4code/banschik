from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Settings

admin.site.register(Settings, SingletonModelAdmin)

config = Settings.get_solo()