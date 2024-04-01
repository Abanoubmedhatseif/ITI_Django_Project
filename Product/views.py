from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from Product.models import Product
from Categories.models import Category  
from Product.serializers import ProductSerializer
from Categories.serializers import CategorySerializer  
from rest_framework.renderers import JSONRenderer
from rest_framework import status

@api_view(['GET'])
def product_and_category_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    products = Product.objects.all()
    categories = Category.objects.all()
    
    result_page = paginator.paginate_queryset(products, request)
    product_serializer = ProductSerializer(result_page, many=True)
    
    result_page = paginator.paginate_queryset(categories, request)
    category_serializer = CategorySerializer(result_page, many=True)

    data = {
        'products': product_serializer.data,
        'categories': category_serializer.data
    }
    return paginator.get_paginated_response(data)

@api_view(['GET'])
def product_search(request):
    query = request.GET.get('q', '')
    if not query:
        return Response({'error': 'Query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)

    products = Product.objects.filter(name__icontains=query)
    serializer = ProductSerializer(products, many=True)
    if not products:
        return Response({'message': 'No products found matching the query'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
