from rest_framework.views import APIView
from rest_framework.response import Response
from orders_application.models import Order
from orders_application.serializers import *
from django.db import transaction
from ecommerce_services.models import product_inventory
from admins_application.serializers import *
from rest_framework import status


class AdminOrderListAPIView(APIView):

    def get(self, request):
        qs = Order.objects.all().order_by("-created_at")

        status_filter = request.GET.get("status")
        payment_filter = request.GET.get("payment")

        if status_filter:
            qs = qs.filter(order_status=status_filter)

        if payment_filter:
            qs = qs.filter(payment_method=payment_filter)

        serializer = AdminOrderSerializer(qs, many=True)
        return Response(serializer.data)


class AdminUpdateOrderStatusAPIView(APIView):

    def patch(self, request, order_id):
        new_status = request.data.get("status")

        if new_status not in ["SHIPPED", "DELIVERED", "CANCELLED", "RTO"]:
            return Response({"error": "Invalid status"}, status=400)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        with transaction.atomic():
            if new_status in ["CANCELLED", "RTO"] and order.order_status not in ["CANCELLED", "RTO"]:
                for item in order.items.select_for_update():
                    inv = item.product_inventory
                    inv.available_quantity += item.quantity
                    inv.save()

            order.order_status = new_status
            order.save()

        return Response({"message": "Order status updated"})

class AdminOrderDetailAPIView(APIView):

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        serializer = AdminOrderSerializer(order)
        return Response(serializer.data)


class AdminOrderStatsAPIView(APIView):

    def get(self, request):
        return Response({
            "total_orders": Order.objects.count(),
            "placed": Order.objects.filter(order_status="PLACED").count(),
            "shipped": Order.objects.filter(order_status="SHIPPED").count(),
            "rto": Order.objects.filter(order_status="RTO").count(),
            "cancelled": Order.objects.filter(order_status="CANCELLED").count(),
        })


class CancelOrderAPIView(APIView):

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        if not order.can_cancel():
            return Response(
                {"error": "Order cannot be cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            for item in order.items.select_for_update():
                inventory = item.product_inventory
                inventory.available_quantity += item.quantity
                inventory.save()

            order.order_status = "CANCELLED"
            order.save()

        return Response({"message": "Order cancelled & stock restored"})
    
class MarkOrderRTOAPIView(APIView):

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        if order.order_status != "SHIPPED":
            return Response(
                {"error": "Only shipped orders can be RTO"},
                status=400
            )

        with transaction.atomic():
            for item in order.items.select_for_update():
                inventory = item.product_inventory
                inventory.available_quantity += item.quantity
                inventory.save()

            order.order_status = "RTO"
            order.save()

        return Response({"message": "Order marked RTO & stock restored"})
