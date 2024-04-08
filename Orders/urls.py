from django.urls import path
from .views import order_list, order_detail, confirm_order, create_checkout_session

urlpatterns = [
    path('confirm-order/', confirm_order, name='confirm-order'),  
    path('orders/', order_list, name='order-list'),  
    path('orders/<str:pk>/', order_detail, name='order-detail'),  
    path('checkout/', create_checkout_session, name='create-checkout-session'),  
]
