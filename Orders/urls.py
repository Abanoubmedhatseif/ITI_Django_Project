from django.urls import path
from .views import order_list, order_detail

urlpatterns = [
    path('orders/', order_list, name='order-list'),
    path('orders/<str:pk>/', order_detail, name='order-detail'),
]
