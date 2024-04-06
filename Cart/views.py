from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

# from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .service import Cart
from Product.models import Product
from Product.serializers import ProductSerializer


@authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
def cart(request):
    if request.method == "GET":
        cart = Cart(request)
        cart_data = list(cart.__iter__())
        cart_total_price = cart.get_total_price()
        return Response(
            {"data": cart_data, "cart_total_price": cart_total_price},
            status=status.HTTP_200_OK,
        )

    elif request.method == "POST":
        cart = Cart(request)

        if "remove" in request.data:
            product = request.data["product"]
            cart.remove(product)

        elif "clear" in request.data:
            cart.clear()

        else:
            product_id = request.data.get("product_id")
            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )

            cart.add(
                product=ProductSerializer(product).data,
                quantity=request.data.get("quantity", 1),
                overide_quantity=request.data.get("overide_quantity", False),
            )

        return Response({"message": "cart updated"}, status=status.HTTP_202_ACCEPTED)
