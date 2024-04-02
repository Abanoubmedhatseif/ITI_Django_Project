from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

# from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from Product.models import Product


@api_view(["GET", "POST", "PUT", "DELETE"])
@authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
def cart(request):
    if request.method == "GET":

        cart_data = request.session.get("cart", {})
        return Response(cart_data)

    elif request.method == "POST":
        product_id = request.data.get("product_id")

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serialized_product = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            # "image_url": product.image.url,
            "category_id": product.category_id,
            "active": product.active,
            "stock": product.stock,
        }

        cart_session = request.session.get("cart", {})
        cart_session.update({product_id: serialized_product})
        request.session["cart"] = cart_session
        request.session.save()
        # Print the session keys
        print(request.session.keys())

        # Print the session items
        for key, value in request.session.items():
            print(f"{key}: {value}")

        return Response(cart_session, status=status.HTTP_201_CREATED)

    elif request.method == "DELETE":
        cart_data = request.session.get("cart", {})
        item_to_remove = request.data.get("item_id")
        if item_to_remove in cart_data:
            del cart_data[item_to_remove]
            request.session["cart"] = cart_data
            return Response(cart_data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND
            )
