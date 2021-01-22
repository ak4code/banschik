from django.urls import path
from .views import HomePage, PageView

app_name = 'cms'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('<slug:slug>/', PageView.as_view(), name='page')
]