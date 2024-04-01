from django.urls import path
from .views import product_and_category_list,product_search, product_detail
from django.urls import path

urlpatterns = [
    path('', product_and_category_list, name='product-and-category-list'),
    path('search/', product_search, name='product-search'),  # Define a separate path for the search endpoint
    path('<str:pk>/', product_detail, name='product-detail'),
]

