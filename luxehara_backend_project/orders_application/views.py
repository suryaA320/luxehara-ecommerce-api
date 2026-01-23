from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders_application.models import Order, OrderItem
from ecommerce_services.models import product_inventory

class PlaceOrderAPIView(APIView):

    def post(self, request):
        data = request.data

        with transaction.atomic():

            order = Order.objects.create(
                customer_name=data["customer_name"],
                customer_email=data["email"],
                customer_mobile=data["mobile"],
                address_line=data["address"],
                city=data["city"],
                state=data["state"],
                pincode=data["pincode"],
                payment_method=data["payment_method"],
                total_amount=data["total_amount"],
                payment_status=(data["payment_method"] == "PREPAID")
            )

            for item in data["items"]:
                inventory = product_inventory.objects.select_for_update().get(
                    id=item["inventory_id"]
                )

                if inventory.available_quantity < item["quantity"]:
                    return Response(
                        {"error": "Out of stock"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                inventory.available_quantity -= item["quantity"]
                inventory.save()

                OrderItem.objects.create(
                    order=order,
                    product_inventory=inventory,
                    quantity=item["quantity"],
                    price_per_unit=item["price"]
                )

        return Response(
            {"message": "Order placed successfully", "order_id": order.id},
            status=status.HTTP_201_CREATED
        )


    
