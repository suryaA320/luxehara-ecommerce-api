from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from orders_application.models import *
from ecommerce_services.models import product_inventory
from rest_framework.exceptions import ValidationError
from orders_application.utils import get_or_create_cart


class PlaceOrderAPIView(APIView):

    @transaction.atomic
    def post(self, request):
        data = request.data

        total_amount = 0
        locked_items = []

        # 🔒 Lock inventory rows
        for item in data["items"]:
            inventory = product_inventory.objects.select_for_update().get(
                id=item["inventory_id"]
            )

            if inventory.available_quantity < item["quantity"]:
                raise ValidationError(
                    f"Out of stock for {inventory.product.product_name}"
                )

            line_total = inventory.selling_price * item["quantity"]
            total_amount += line_total

            locked_items.append({
                "inventory": inventory,
                "quantity": item["quantity"],
                "price": inventory.selling_price
            })

        # 🧾 Create Order
        order = Order.objects.create(
            customer_name=data["customer_name"],
            customer_email=data["customer_email"],
            customer_mobile=data["customer_mobile"],
            address_line=data["address"],
            city=data["city"],
            state=data["state"],
            pincode=data["pincode"],
            payment_method=data["payment_method"],
            payment_status=(data["payment_method"] == "PREPAID"),
            total_amount=total_amount
        )

        # 📦 Create Order Items + update stock
        for item in locked_items:
            inventory = item["inventory"]

            inventory.available_quantity -= item["quantity"]
            inventory.save()

            OrderItem.objects.create(
                order=order,
                product_inventory=inventory,
                quantity=item["quantity"],
                price_per_unit=item["price"]
            )

        return Response(
            {
                "message": "Order placed successfully",
                "order_id": order.id,
                "total_amount": total_amount
            },
            status=status.HTTP_201_CREATED
        )

    
class AddToCartAPIView(APIView):

    def post(self, request):
        print("ADD → session:", request.session.session_key)
        cart = get_or_create_cart(request)
        print("ADD → cart id:", cart.id)

        inventory_id = request.data["inventory_id"]
        quantity = request.data.get("quantity", 1)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_inventory_id=inventory_id,
            defaults={"quantity": quantity}
        )
        print("ADD → cart item:", cart_item.id)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({"message": "Added to cart"})


class ViewCartAPIView(APIView):

    def get(self, request):
        print("VIEW → session:", request.session.session_key)

        cart = get_or_create_cart(request)
        print("VIEW → cart id:", cart.id)

        items = []
        total = 0
        for item in cart.items.select_related(
            "product_inventory__product",
            "product_inventory__color",
            "product_inventory__size"
        ):
            line_total = item.quantity * item.product_inventory.selling_price
            total += line_total

            items.append({
                "id": item.id,
                "inventory_id": item.product_inventory.id,
                "product_name": item.product_inventory.product.product_name,
                "color": item.product_inventory.color.color_details,
                "size": item.product_inventory.size.size,
                "price": item.product_inventory.selling_price,
                "quantity": item.quantity,
                "line_total": line_total
            })

        return Response({"items": items, "total": total})


class UpdateCartItemAPIView(APIView):

    def patch(self, request, item_id):
        quantity = request.data["quantity"]

        if quantity < 1:
            return Response({"error": "Invalid quantity"}, status=400)

        item = CartItem.objects.get(id=item_id)
        item.quantity = quantity
        item.save()

        return Response({"message": "Updated"})


class RemoveCartItemAPIView(APIView):

    def delete(self, request, item_id):
        CartItem.objects.filter(id=item_id).delete()
        return Response({"message": "Removed"})
