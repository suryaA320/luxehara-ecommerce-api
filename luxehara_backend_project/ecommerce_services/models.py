from django.db import models
import uuid

# Create your models here.

class categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=30, blank=False, null=False)
    category_description = models.TextField(max_length=300, default='')

    def __str__(self):
        return self.category_name
    
class colors_available(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    color_details = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.color_details
    
class size_details(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    size = models.CharField(max_length=10, default='')

    def __str__(self):
        return self.size
    
class product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=50)
    product_sku = models.CharField(max_length=10, unique=True)
    product_description = models.TextField(max_length=1200)
    product_category = models.ForeignKey(categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

class product_inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    product = models.ForeignKey(
        product,
        on_delete=models.CASCADE,
        related_name="inventory"
    )

    color = models.ForeignKey(colors_available, on_delete=models.CASCADE)
    size = models.ForeignKey(size_details, on_delete=models.CASCADE)

    available_quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ("product", "color", "size")

    def __str__(self):
        return f"{self.product.product_name} | {self.color} | {self.size} | {self.available_quantity}"



class product_images(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_fk = models.ForeignKey(product, on_delete=models.CASCADE, related_name="products_image_relation")
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.product_fk