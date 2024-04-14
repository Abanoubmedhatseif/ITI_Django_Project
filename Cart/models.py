from django.db import models
from django.utils import timezone
from User.models import CustomUser  # Import your User model
from Product.models import Product  # Import your Product model


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"

    @property
    def user(self):
        return self.cart.user if self.cart else None
