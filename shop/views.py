from django.views.generic import DetailView
from .models import Category, Product


class CategoryDetail(DetailView):
    model = Category
    queryset = Category.objects.prefetch_related('products')


class ProductDetail(DetailView):
    model = Product
    queryset = Product.objects.select_related('category')
    slug_field = 'category__slug'
    query_pk_and_slug = True
