from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer
from rest_framework.pagination import PageNumberPagination


@api_view(['GET'])
def category_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10 

    categories = Category.objects.all()
    result_page = paginator.paginate_queryset(categories, request)

    serializer = CategorySerializer(result_page, many=True)
    
    return paginator.get_paginated_response(serializer.data)
