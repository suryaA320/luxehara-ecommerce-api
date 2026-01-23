from rest_framework import serializers
from orders_application.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product_inventory.product.product_name",
        read_only=True
    )
    color = serializers.CharField(
        source="product_inventory.color.color_details",
        read_only=True
    )
    size = serializers.CharField(
        source="product_inventory.size.size",
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product_name",
            "color",
            "size",
            "quantity",
            "price_per_unit",
        )