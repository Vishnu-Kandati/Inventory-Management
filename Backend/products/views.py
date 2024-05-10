from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .utils import create_user_account
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .pagination import CustomLimitOffsetPagination

@api_view(['POST'])
def create_user(request):
    """
    API endpoint for creating a new user.
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            if username and email and password:
                create_user_account(username, email, password)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## Implementation of 'GET', 'POST', 'PUT', 'DELETE' for the Item and 'POST' for Category
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def detail_view(request, sku=None, model_cls=None, serializer_cls=None):
    if request.method == 'GET':
        item = None
        if sku is not None:
            item= model_cls.objects.filter(sku=sku).first()
            if item is not None:
                serializer = serializer_cls(item)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Get query parameters for filtering
            category = request.query_params.get('category', None)
            stock_status = request.query_params.get('stock_status', None)
            start_date = request.query_params.get('start_date', None)
            end_date = request.query_params.get('end_date', None)

            # Filter items based on query parameters
            items = model_cls.objects.all()
            if category:
                items = items.filter(category=category)
            if stock_status:
                items = items.filter(stock_status=stock_status)
            if start_date and end_date:
                items = items.filter(created_at__range=[start_date, end_date])

            # Paginate the data
            paginator = CustomLimitOffsetPagination()
            paginated_data = paginator.paginate_queryset(items, request)
            serializer = serializer_cls(paginated_data, many=True)
            return paginator.get_paginated_response(serializer.data)
        
    elif request.method == 'POST':
        serializer = serializer_cls(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            serialized_data = serializer_cls(item).data
            return Response(serialized_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method in ['PUT', 'DELETE']:
        item = None
        if sku is not None:
            item = model_cls.objects.filter(sku=sku).first()
        if item is None:
            return Response({'detail': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'PUT':
            serializer = serializer_cls(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
