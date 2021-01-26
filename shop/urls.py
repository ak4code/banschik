from django.urls import path
from .views import CategoryDetail, ProductDetail

app_name = 'shop'

urlpatterns = [
    path('<slug:slug>/', CategoryDetail.as_view(), name='category'),
    path('<slug:slug>/<int:pk>/', ProductDetail.as_view(), name='product'),
]
