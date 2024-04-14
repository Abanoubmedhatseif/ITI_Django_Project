from rest_framework import serializers
from .models import Order
from Product.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
