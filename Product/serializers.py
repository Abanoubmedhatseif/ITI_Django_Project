from rest_framework import serializers
from .models import Product  # Adjusted import path

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        