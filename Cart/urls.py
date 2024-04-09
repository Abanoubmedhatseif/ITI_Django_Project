from django.urls import path
from .views import cartAPI

urlpatterns = [
    path("cart/", cart, name="cart"),
]
