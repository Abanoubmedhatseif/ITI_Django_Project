from django.urls import path
from .views import product_list,product_search, product_detail,products_by_category
from django.urls import path

urlpatterns = [
    path('products/', product_list, name='product'),
    path('search/', product_search, name='product-search'),
    path('products/<str:pk>/', product_detail, name='product-detail'),
    path('products/categories/<str:category_id>/', products_by_category, name='products_by_category'),
]

