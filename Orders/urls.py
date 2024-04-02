from django.urls import path
from .views import order_list, order_detail, confirm_order

urlpatterns = [
    path("confirm-order/", confirm_order, name="confirm-order"),  # user
    path("orders/", order_list, name="order-list"),  # user
    path(
        "orders/<str:pk>/", order_detail, name="order-detail"
    ),  # user--> get order_detail
]
