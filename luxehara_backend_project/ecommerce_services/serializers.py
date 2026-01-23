from rest_framework import serializers
from ecommerce_services.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = categories
        fields = ("id", "category_name", "category_description")

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = colors_available
        fields = ("id", "color_details")


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = size_details
        fields = ("id", "size")

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_images
        fields = ("id", "is_primary")

class ProductInventorySerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)

    class Meta:
        model = product_inventory
        fields = (
            "id",
            "color",
            "size",
            "available_quantity",
        )

class ProductSerializer(serializers.ModelSerializer):
    inventory = ProductInventorySerializer(many=True, read_only=True)
    products_image_relation = ProductImageSerializer(many=True, read_only=True)
    product_category = CategorySerializer(read_only=True)

    class Meta:
        model = product
        fields = (
            "id",
            "product_name",
            "product_sku",
            "product_description",
            "product_category",
            "inventory",
            "products_image_relation",
        )
