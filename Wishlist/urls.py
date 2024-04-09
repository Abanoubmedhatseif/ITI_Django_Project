from django.urls import path
from .views import wishListAPI

urlpatterns = [
    path('wishlist', wishListAPI, name='wishlist-api'),
]
