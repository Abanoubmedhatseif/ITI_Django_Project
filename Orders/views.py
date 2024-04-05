from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Order
from .serializers import OrderSerializer
from Product.models import Product
from rest_framework.request import Request  
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication,BasicAuthentication


@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        return confirm_order(request)

@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def confirm_order(request: Request):  
    print("before confirm_order")
    if request.data.get('confirm_order') == 'true':
        print("after confirm_order")
        cart_data = request.session.get('cart', {})
        total_price = 0

        for product in cart_data.values():
            try:
                total_price += float(product['price'])
            except ValueError:
                return Response({'error': 'Invalid price format'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
            )
            for product in cart_data.values():
                order.products.add(Product.objects.get(pk=product['id']))

        request.session["cart"] = {}

        return Response(
            {"message": "Order created successfully"},
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response({'error': 'confirm_order must be true'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
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
