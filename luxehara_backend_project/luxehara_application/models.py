from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.

class User(AbstractUser):
    SUPER_ADMIN = 1
    STAFF = 2
    CUSTOMER = 3
    MANAGER = 4


    ROLE_CHOICES = (
        (SUPER_ADMIN, 'SuperAdmin'),
        (STAFF, 'Staff'),
        (CUSTOMER, 'Customer'),
        (MANAGER, 'Manager'),

    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3)
    mobile_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    user_status = models.CharField(max_length=10, default='Inactive')
    alternate_number = models.CharField(max_length=15, default='')
    created_at = models.DateTimeField(auto_now_add=True)  # Stores when the record was created
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["mobile_number", "first_name", "last_name"]