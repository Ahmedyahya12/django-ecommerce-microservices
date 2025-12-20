from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from catalog.filters import ProductFilter
from catalog.models import Product
from catalog.serializers import ProductDetailSerializer, ProductListSerializer
from django.db.models import Q


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def get_products(request):
    products = Product.objects.filter(available=True)
    qs_filtered = ProductFilter(request.GET, queryset=products).qs
    serializer = ProductListSerializer(qs_filtered, many=True)
    return Response({"products": serializer.data})


@api_view(["GET"])
def get_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    serializer = ProductDetailSerializer(product)
    return Response({"product": serializer.data})


@api_view(["GET"])
def search_products(request):
    """Search products by name or category."""

    query = request.query_params.get("query")
    if not query:
        return Response(
            {"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    qs_filtered = Product.objects.filter(
        Q(name__icontains=query) | Q(category__name__icontains=query)
    )

    serializer = ProductListSerializer(qs_filtered, many=True)
    return Response({"products": serializer.data})
