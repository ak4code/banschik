from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django_email_verification import urls as email_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('email/', include(email_urls)),
    path('tinymce/', include('tinymce.urls')),
    path('catalog/', include('shop.urls')),
    path('', include('cms.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.extend([path('__debug__/', include(debug_toolbar.urls)), ])
