from .models import Product
from .models import Wishlist
from .serializers import WishlistSerializer
from Product.serializers import ProductSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET','POST','DELETE'])
# @permission_classes([IsAuthenticated])
def wishListAPI(request):
    if request.method == "GET":
        # wishlist = Wishlist.objects.filter(user=request.user).first()
        wishlist = Wishlist.objects.first()
        if not wishlist:
            return Response({"message": "Wishlist does not exist for this user."}, status=404)
        
        products = wishlist.products.all()
        product_data = []
        
        # Serialize each product and collect the serialized data
        for product in products:
            product_serializer = ProductSerializer(product)
            product_data.append(product_serializer.data)
        
        # Return the serialized product data as part of the response
        return Response(product_data)

    elif request.method == "POST":
        data = request.data
        product_id = data.get('product_id')
        # wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist, created = Wishlist.objects.get_or_create(user=1)
        wishlist.products.add(product_id)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=201)

    elif request.method == "DELETE":
        data = request.data
        product_id = data.get('product_id')
        try:
            wishlist = Wishlist.objects.get(user=1)
            # wishlist = Wishlist.objects.first()
            product = wishlist.products.get(pk=product_id)
        except Wishlist.DoesNotExist:
            return Response({'error': 'Wishlist not found'}, status=404)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found in wishlist'}, status=404)
        
        wishlist.products.remove(product)
        return Response({'message': 'Product removed from wishlist successfully'}, status=204)