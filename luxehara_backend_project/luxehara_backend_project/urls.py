"""
URL configuration for luxehara_backend_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from luxehara_application.views import *
from orders_application.views import *
from admins_application.views import *
from ecommerce_services.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/token/login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("api/token/refresh/", RefreshTokenView.as_view(), name="refresh_token"),
    path("register/", RegisterView.as_view(), name="register"),

    # INVENTORY
    path("categories/", CategoryListAPIView.as_view()),
    path("products/", ProductListAPIView.as_view()),
    path("products/<uuid:product_id>/", ProductDetailAPIView.as_view()),

    # Admin
    path("inventory/create/", CreateProductInventoryAPIView.as_view()),
    path("inventory/<uuid:inventory_id>/update/", UpdateInventoryStockAPIView.as_view()),
    path("admin/orders/<uuid:order_id>/cancel/",CancelOrderAPIView.as_view(),name="admin-cancel-order"),

    # Admin / Ops – Mark RTO
    path("admin/orders/<uuid:order_id>/rto/",MarkOrderRTOAPIView.as_view(),name="admin-mark-rto"),

    # Orders
    path("admin/orders/", AdminOrderListAPIView.as_view()),
    path("admin/orders/stats/", AdminOrderStatsAPIView.as_view()),
    path("admin/orders/<uuid:order_id>/", AdminOrderDetailAPIView.as_view()),
    path("admin/orders/<uuid:order_id>/status/", AdminUpdateOrderStatusAPIView.as_view()),
]
