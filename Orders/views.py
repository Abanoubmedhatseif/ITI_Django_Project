from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Order
from .serializers import OrderSerializer
from Product.models import Product
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import PermissionDenied
import stripe
from django.conf import settings


@api_view(["GET", "POST"])
def order_list(request):
    if request.method == "GET":
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        return confirm_order(request)


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def confirm_order(request: Request):
    print("before confirm_order")
    try:
        if request.data.get("confirm_order") == "true":
            print("after confirm_order")
            cart_data = request.session.get("cart", {})
            total_price = 0

            for product in cart_data.values():
                try:
                    total_price += float(product["price"])
                except ValueError:
                    return Response(
                        {"error": "Invalid price format"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    total_price=total_price,
                )
                for product in cart_data.values():
                    order.products.add(Product.objects.get(pk=product["id"]))

            request.session["cart"] = {}

            return Response(
                {"message": "Order created successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": "confirm_order must be true"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except PermissionDenied:
        return Response(
            {"error": "You need to be authenticated to confirm the order"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    except ValueError as e:
        if "AnonymousUser" in str(e):
            return Response(
                {"error": "You need to be authenticated to confirm the order"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            return Response(
                {"error": "An error occurred while processing your request"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def create_checkout_session(request):
    cart_data = request.session.get("cart", {})
    total_price = sum(float(product["price"]) for product in cart_data.values())

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(total_price * 100),
                        "product_data": {
                            "name": "Order",
                            "description": "Items in your order",
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return Response(
            {"sessionId": checkout_session.id}, status=status.HTTP_201_CREATED
        )
    except stripe.error.StripeError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PATCH":
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
