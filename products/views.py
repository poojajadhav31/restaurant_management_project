from rest_framework import viewsets, status
from datetime import date
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from .serializers import ProductUpdateSerializer
from .models import Product
from .models import Special

@api_view(['GET'])
def menu_api(request):
    menu = [
        {
            "name" : "Panner Butter Masala",
            "description" : "Soft panner cubs in creamy tomato gravy",
            "price" : "180.00"
        },

        {
            "name" : "Veg Biryani",
            "description" : "Aromatic rice with mixed vegetables and spices",
            "price" : "150.00"
        },

        {
            "name" : "Masala Dosa",
            "description" : "Crispy dosa stuffed with spicy mashed potatoes",
            "price" : 70.00
        }

    ]
    # Get page number from request ( default = 1 )
    page_number = request.GET.get('page',1)
    paginator = Paginator(menu, 2 )

    try:
        page_obj = paginator.page(page_number)
    except:
        page_obj = paginator.page(1)

    data = {
        "count": paginator.count,
        "total_pages": page_obj.number,
        "current_page": page_obj.number,
        "results": list(page_obj.object_list),
    }
    return Response(data)
def products_by_category(request):
    category_name = request.query_params.get('category', None)
    
    if not category_name:
        return Response({"error": "Category parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    products = Product.objects.filter(category__category_name__iexact=category_name)
    
    if not products.exists():
        return Response({"message": f"No products found for category '{category_name}'"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def todays_specials(request):
    specials = Special.objects.filter(date=date.today())

    return render(request,'products/specials.html',{'specials':specials})

def about_chefs(request):
    from .models import Chef
    chefs = Chef.objects.all()
    return render(request,'products/chefs.html',{'chefs':chefs})

class ProductPagination(PageNumberPagination):
    page_size = 5   # adjust per page items
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductSearchViewSet(viewsets.ViewSet):
    pagination_class = ProductPagination

    def list(self, request):
        query = request.query_params.get('q', '')  # search query
        products = Product.objects.filter(name__icontains=query)

        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def product_search(self, request):
        query = request.GET.get('q', '')
        products = Product.objects.filter(name__icontains=query)
        return render(request, 'products/product_list.html', {'products': products, 'query': query})
    
class ProductUpdateViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]  # Only admin can update

    def update(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductUpdateSerializer(product, data=request.data, partial=True)  # partial=True allows PATCH
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Product updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)