from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ecommerce_services.models import *
from ecommerce_services.serializers import *
from django.db import transaction
import json



# Create your views here.


# LIST CATEGORIES
class CategoryListAPIView(APIView):

    def get(self, request):
        qs = categories.objects.all()
        serializer = CategorySerializer(qs, many=True)
        return Response(serializer.data)

# POST CATEGORY   
class CategoryCreateAPIView(APIView):

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#  FETCH SINGLE CATEGORY
class CategoryDetailAPIView(APIView):

    def get(self, request, category_id):
        try:
            category = categories.objects.get(id=category_id)
        except categories.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


# PUT/PATCH
class CategoryUpdateAPIView(APIView):

    def put(self, request, category_id):
        try:
            category = categories.objects.get(id=category_id)
        except categories.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, category_id):
        try:
            category = categories.objects.get(id=category_id)
        except categories.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(category, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE CATEGORY
class CategoryDeleteAPIView(APIView):

    def delete(self, request, category_id):
        try:
            category = categories.objects.get(id=category_id)
        except categories.DoesNotExist:
            return Response(
                {"error": "Category not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        category.delete()
        return Response(
            {"message": "Category deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

# ************************************************************** COLORS ******************************************************
# CREATE COLOR
class ColorCreateAPIView(APIView):

    def post(self, request):
        serializer = ColorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# LIST COLORS
class ColorListAPIView(APIView):

    def get(self, request):
        qs = colors_available.objects.all()
        serializer = ColorSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# COLOR DETAIL
class ColorDetailAPIView(APIView):

    def get(self, request, color_id):
        try:
            color = colors_available.objects.get(id=color_id)
        except colors_available.DoesNotExist:
            return Response(
                {"error": "Color not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ColorSerializer(color)
        return Response(serializer.data, status=status.HTTP_200_OK)


# UPDATE COLOR
class ColorUpdateAPIView(APIView):

    def put(self, request, color_id):
        try:
            color = colors_available.objects.get(id=color_id)
        except colors_available.DoesNotExist:
            return Response(
                {"error": "Color not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ColorSerializer(color, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, color_id):
        try:
            color = colors_available.objects.get(id=color_id)
        except colors_available.DoesNotExist:
            return Response(
                {"error": "Color not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ColorSerializer(color, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE COLOR
class ColorDeleteAPIView(APIView):

    def delete(self, request, color_id):
        try:
            color = colors_available.objects.get(id=color_id)
        except colors_available.DoesNotExist:
            return Response(
                {"error": "Color not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        color.delete()
        return Response(
            {"message": "Color deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
# ************************************************************** SIZES ******************************************************

# CREATE SIZE
class SizeCreateAPIView(APIView):

    def post(self, request):
        serializer = SizeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# LIST SIZES
class SizeListAPIView(APIView):

    def get(self, request):
        qs = size_details.objects.all()
        serializer = SizeSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# SIZE DETAIL
class SizeDetailAPIView(APIView):

    def get(self, request, size_id):
        try:
            size = size_details.objects.get(id=size_id)
        except size_details.DoesNotExist:
            return Response(
                {"error": "Size not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SizeSerializer(size)
        return Response(serializer.data, status=status.HTTP_200_OK)


# UPDATE SIZE
class SizeUpdateAPIView(APIView):

    def put(self, request, size_id):
        try:
            size = size_details.objects.get(id=size_id)
        except size_details.DoesNotExist:
            return Response(
                {"error": "Size not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SizeSerializer(size, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, size_id):
        try:
            size = size_details.objects.get(id=size_id)
        except size_details.DoesNotExist:
            return Response(
                {"error": "Size not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SizeSerializer(size, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE SIZE
class SizeDeleteAPIView(APIView):

    def delete(self, request, size_id):
        try:
            size = size_details.objects.get(id=size_id)
        except size_details.DoesNotExist:
            return Response(
                {"error": "Size not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        size.delete()
        return Response(
            {"message": "Size deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
    
# ************************************************************** PRODUCTS ******************************************************
# create product
class ProductCreateAPIView(APIView):

    @transaction.atomic
    def post(self, request):
        try:
            product_raw = request.data.get("product")
            inventory_raw = request.data.get("inventory")

            if not product_raw or not inventory_raw:
                raise ValidationError("Product or inventory data missing")

            product_data = json.loads(product_raw)
            inventory_data = json.loads(inventory_raw)

            images = json.loads(request.data.get("images", "[]"))
            primary_index = int(request.data.get("primary_index", 0))

            # 1️⃣ Save Product
            product_serializer = ProductSerializer(data=product_data)
            product_serializer.is_valid(raise_exception=True)
            product_obj = product_serializer.save()

            # 2️⃣ Save Inventory
            for item in inventory_data:
                product_inventory.objects.create(
                    product=product_obj,
                    color_id=item["color"],
                    size_id=item["size"],
                    cost_price=item.get("cost_price", 0),
                    selling_price=item.get("selling_price", 0),
                    max_price=item.get("max_price", 0),
                    available_quantity=item["available_quantity"],
                )

            # 3️⃣ Save Images
            for img in images:
                product_images.objects.create(
                    product_fk=product_obj,
                    image_url=img["image_url"],
                    is_primary=img.get("is_primary", False)
                )


            return Response(
                ProductSerializer(product_obj).data,
                status=status.HTTP_201_CREATED
            )

        except ValidationError:
            raise  # DRF will handle correctly

        except Exception as e:
            raise ValidationError(str(e))



# list product
class ProductListAPIView(APIView):

    def get(self, request):
        qs = product.objects.all()
        serializer = ProductSerializer(qs, many=True)
        return Response(serializer.data)
    
# product details
class ProductDetailAPIView(APIView):

    def get(self, request, product_id):
        try:
            prod = product.objects.get(id=product_id)
        except product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        serializer = ProductSerializer(prod)
        return Response(serializer.data)


# put/patch product
class ProductUpdateAPIView(APIView):

    @transaction.atomic
    def put(self, request, product_id):

        try:
            prod = product.objects.select_for_update().get(id=product_id)
        except product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        data = request.data  # ✅ already parsed JSON

        # ---------------- PRODUCT ----------------
        product_data = data.get("product", {})

        prod.product_name = product_data.get("product_name", prod.product_name)
        prod.product_sku = product_data.get("product_sku", prod.product_sku)
        prod.product_description = product_data.get(
            "product_description", prod.product_description
        )

        if product_data.get("product_category"):
            prod.product_category_id = product_data["product_category"]

        prod.save()

        # ---------------- INVENTORY ----------------
        inventory_data = data.get("inventory", [])
        keep_inventory_ids = []

        for item in inventory_data:
            inv_id = item.get("id")

            if inv_id:
                inv = product_inventory.objects.select_for_update().get(
                    id=inv_id, product=prod
                )
            else:
                inv = product_inventory(product=prod)

            inv.color_id = item["color"]
            inv.size_id = item["size"]
            inv.cost_price = item["cost_price"]
            inv.selling_price = item["selling_price"]
            inv.max_price = item["max_price"]
            inv.available_quantity = item["available_quantity"]
            inv.save()

            keep_inventory_ids.append(inv.id)

        product_inventory.objects.filter(product=prod).exclude(
            id__in=keep_inventory_ids
        ).delete()

        # ---------------- IMAGES (URL BASED) ----------------
        existing_images = data.get("existing_images", [])
        new_image_urls = data.get("new_image_urls", [])
        primary_index = data.get("primary_index", 0)

        product_images.objects.filter(product_fk=prod).delete()

        all_images = []

        for img in existing_images:
            all_images.append(img["image_url"])

        for url in new_image_urls:
            all_images.append(url)

        for index, url in enumerate(all_images):
            product_images.objects.create(
                product_fk=prod,
                image_url=url,
                is_primary=(index == primary_index)
            )

        return Response(
            ProductSerializer(prod).data,
            status=status.HTTP_200_OK
        )
    
    

# delete product
class ProductDeleteAPIView(APIView):

    def delete(self, request, product_id):
        try:
            prod = product.objects.get(id=product_id)
        except product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        prod.delete()
        return Response({"message": "Product deleted"}, status=204)


# ************************************************************** INVENTORY ******************************************************

# create Inventory
class ProductInventoryCreateAPIView(APIView):

    def post(self, request):
        serializer = ProductInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# List inventory
class ProductInventoryListAPIView(APIView):

    def get(self, request):
        product_id = request.GET.get("product")
        qs = product_inventory.objects.all()

        if product_id:
            qs = qs.filter(product_id=product_id)

        serializer = ProductInventorySerializer(qs, many=True)
        return Response(serializer.data)

# inventory details
class ProductInventoryDetailAPIView(APIView):

    def get(self, request, inventory_id):
        try:
            inventory = product_inventory.objects.get(id=inventory_id)
        except product_inventory.DoesNotExist:
            return Response({"error": "Inventory not found"}, status=404)

        serializer = ProductInventorySerializer(inventory)
        return Response(serializer.data)


# update inventory
class ProductInventoryUpdateAPIView(APIView):

    def patch(self, request, inventory_id):
        try:
            inventory = product_inventory.objects.get(id=inventory_id)
        except product_inventory.DoesNotExist:
            return Response({"error": "Inventory not found"}, status=404)

        serializer = ProductInventorySerializer(
            inventory,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

# Delete Inventory
class ProductInventoryDeleteAPIView(APIView):

    def delete(self, request, inventory_id):
        try:
            inventory = product_inventory.objects.get(id=inventory_id)
        except product_inventory.DoesNotExist:
            return Response({"error": "Inventory not found"}, status=404)

        inventory.delete()
        return Response({"message": "Inventory deleted"}, status=204)

# upload image
class ProductImageCreateAPIView(APIView):

    def post(self, request):
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# list product images
class ProductImageListAPIView(APIView):

    def get(self, request, product_id):
        qs = product_images.objects.filter(product_fk_id=product_id)
        serializer = ProductImageSerializer(qs, many=True)
        return Response(serializer.data)

# update images
class ProductImageUpdateAPIView(APIView):

    def patch(self, request, image_id):
        try:
            image = product_images.objects.get(id=image_id)
        except product_images.DoesNotExist:
            return Response({"error": "Image not found"}, status=404)

        serializer = ProductImageSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

# delete images
class ProductImageDeleteAPIView(APIView):

    def delete(self, request, image_id):
        try:
            image = product_images.objects.get(id=image_id)
        except product_images.DoesNotExist:
            return Response({"error": "Image not found"}, status=404)

        image.delete()
        return Response({"message": "Image deleted"}, status=204)


class ProductFullCreateAPIView(APIView):

    @transaction.atomic
    def post(self, request):
        try:
            product_data = request.data.get("product")
            inventory_data = request.data.get("inventory", [])
            images_data = request.data.get("images", [])

            # 1️⃣ Create Product
            product_serializer = ProductCreateNestedSerializer(data=product_data)
            product_serializer.is_valid(raise_exception=True)
            product_obj = product_serializer.save()

            # 2️⃣ Create Inventory
            for inv in inventory_data:
                inv["product"] = product_obj.id
                inventory_serializer = InventoryNestedSerializer(data=inv)
                inventory_serializer.is_valid(raise_exception=True)
                inventory_serializer.save()

            # 3️⃣ Images (enforce single primary)
            primary_found = False

            for img in images_data:
                if img.get("is_primary") and not primary_found:
                    primary_found = True
                elif img.get("is_primary") and primary_found:
                    img["is_primary"] = False

                product_images.objects.create(
                    product_fk=product_obj,
                    image=img.get("image"),
                    is_primary=img.get("is_primary", False)
                )

            return Response(
                {
                    "message": "Product created successfully",
                    "product_id": product_obj.id
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
