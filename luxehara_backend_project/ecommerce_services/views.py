from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ecommerce_services.models import *
from ecommerce_services.serializers import *

# Create your views here.


# LIST CATEGORIES
class CategoryListAPIView(APIView):

    def get(self, request):
        qs = categories.objects.all()
        serializer = CategorySerializer(qs, many=True)
        return Response(serializer.data)


# LIST PRODUCTS
class ProductListAPIView(APIView):

    def get(self, request):
        category_id = request.GET.get("category")

        qs = product.objects.all()

        if category_id:
            qs = qs.filter(product_category_id=category_id)

        serializer = ProductSerializer(qs, many=True)
        return Response(serializer.data)


# PRODUCT DETAILS API
class ProductDetailAPIView(APIView):

    def get(self, request, product_id):
        try:
            prod = product.objects.get(id=product_id)
        except product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(prod)
        return Response(serializer.data)


# ADMIN/STOCK MANAGEMENT API
class CreateProductInventoryAPIView(APIView):

    def post(self, request):
        serializer = ProductInventorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


# UPDATE STOCK QUANTITY
class UpdateInventoryStockAPIView(APIView):

    def patch(self, request, inventory_id):
        try:
            inventory = product_inventory.objects.get(id=inventory_id)
        except product_inventory.DoesNotExist:
            return Response({"error": "Inventory not found"}, status=404)

        inventory.available_quantity = request.data.get(
            "available_quantity",
            inventory.available_quantity
        )
        inventory.save()

        return Response(
            ProductInventorySerializer(inventory).data
        )
