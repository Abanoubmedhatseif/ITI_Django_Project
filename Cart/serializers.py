from datetime import timezone
from rest_framework import serializers
from .models import Cart, CartItem
from Product.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["user", "created_at", "updated_at"]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Assuming you have a ProductSerializer defined

    class Meta:
        model = CartItem
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new CartItem instance, given the validated data.
        """
        return CartItem.objects.create(
            cart=validated_data["cart"],
            product=validated_data["product"],
            quantity=validated_data.get(
                "quantity", 1
            ),  # Set default quantity to 1 or as needed
            added_at=validated_data.get("added_at", timezone.now()),
        )

    def update(self, instance, validated_data):
        """
        Update and return an existing CartItem instance, given the validated data.
        """
        instance.product = validated_data.get("product", instance.product)
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.added_at = validated_data.get("added_at", instance.added_at)
        instance.save()
        return instance
