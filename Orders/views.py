from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Order
from .serializers import OrderSerializer
from Cart.models import CartItem
from rest_framework.request import Request  
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect

default_payment_method = "cash"

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
def send_order_confirmation_email(user_email):
    subject = 'Order Confirmation'
    message = "Your order has been successfully placed."
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user_email]
    send_mail(subject, message, from_email, to_email)
    
stripe.api_key = settings.STRIPE_SECRET_KEY
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def create_checkout_session(request: Request):
    try:
        cart_id = request.data.get("cart_id")
        if not cart_id:
            return Response(
                {"error": "Cart ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        payment_method = request.data.get("payment_method")
        if payment_method not in ['cash', 'card']:
            return Response(
                {"error": "Invalid payment method"}, status=status.HTTP_400_BAD_REQUEST
            )

        cart_items = CartItem.objects.filter(cart_id=cart_id)
        line_items = []
        total_price = 0
        for cart_item in cart_items:
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(cart_item.product.price * 100),
                    "product_data": {
                        "name": cart_item.product.name,
                        "description": cart_item.product.description,
                    },
                },
                "quantity": cart_item.quantity,
            })
            total_price += cart_item.product.price * cart_item.quantity

        if payment_method == 'cash':
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    total_price=total_price,
                )
                for cart_item in cart_items:
                    order.products.add(cart_item.product)
                    
            send_order_confirmation_email(request.user.email)

            cart_items.delete()

            return Response(
                {"message": "Order created successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=settings.SITE_URL+'/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL+'/?cancel=true',
            )
            
            send_order_confirmation_email(request.user.email)

            cart_items.delete()
            return Response({'url': checkout_session.url}, status=status.HTTP_201_CREATED)
    except stripe.error.StripeError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
