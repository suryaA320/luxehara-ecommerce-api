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
        fields = ("id", "image_url", "is_primary")

class ProductInventorySerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    size = SizeSerializer(read_only=True)

    class Meta:
        model = product_inventory
        fields = (
            "id",
            "color",
            "size",
            "cost_price",
            "selling_price",
            "max_price",
            "available_quantity",
        )

class ProductSerializer(serializers.ModelSerializer):
    # WRITE → accept UUID
    product_category = serializers.PrimaryKeyRelatedField(
        queryset=categories.objects.all(),
        write_only=True
    )

    # READ → return full object
    product_category_details = CategorySerializer(
        source="product_category",
        read_only=True
    )

    inventory = ProductInventorySerializer(many=True, read_only=True)
    products_image_relation = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = product
        fields = (
            "id",
            "product_name",
            "product_sku",
            "product_description",
            "product_category",          # write-only
            "product_category_details",  # read-only
            "inventory",
            "products_image_relation",
        )


class ProductCreateNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = "__all__"

class ProductInventoryWriteSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    color = serializers.UUIDField()
    size = serializers.UUIDField()
    cost_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = serializers.IntegerField()

class ProductUpdateSerializer(serializers.Serializer):
    product_name = serializers.CharField(required=False)
    product_sku = serializers.CharField(required=False)
    product_description = serializers.CharField(required=False)
    product_category = serializers.UUIDField(required=False)

    inventory = ProductInventoryWriteSerializer(many=True, required=False)


class InventoryNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_inventory
        fields = ["color", "size", "available_quantity"]


class ImageNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_images
        fields = ["image", "is_primary"]