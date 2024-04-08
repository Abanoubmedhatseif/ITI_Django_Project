from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem, Cart
from .serializers import CartItemSerializer
from Product.models import Product
from rest_framework.permissions import IsAuthenticated


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def cart(request):
    if request.method == "GET":
        # Filter CartItems by the user associated with the Cart
        cart_items = CartItem.objects.filter(cart__user=request.user)
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        product_id = request.data.get("product_id")
        if not product_id:
            return Response(
                {"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if the product already exists in the cart
        existing_cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if existing_cart_item:
            # Increment the quantity of the existing cart item
            existing_cart_item.quantity += int(request.data.get("quantity", 1))
            existing_cart_item.save()
            serializer = CartItemSerializer(existing_cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If the product is not already in the cart, create a new cart item
        cart_item = CartItem.objects.create(
            product=product,
            quantity=request.data.get("quantity", 1),
            cart=cart,
        )
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == "DELETE":
        item_id = request.data.get("item_id")
        if not item_id:
            return Response(
                {"error": "Item ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cart_item = CartItem.objects.get(pk=item_id, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND
            )

        cart_item.delete()
        return Response(
            {"message": "Cart item deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
