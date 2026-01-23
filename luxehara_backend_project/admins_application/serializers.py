from rest_framework import serializers
from orders_application.models import *
from orders_application.serializers import *

class AdminOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"