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

    # CATEGORY
    path('categories/', CategoryListAPIView.as_view()),
    path('categories/create/', CategoryCreateAPIView.as_view()),
    path('categories/<uuid:category_id>/', CategoryDetailAPIView.as_view()),
    path('categories/<uuid:category_id>/update/', CategoryUpdateAPIView.as_view()),
    path('categories/<uuid:category_id>/delete/', CategoryDeleteAPIView.as_view()),


    # COLORS
    path('colors/', ColorListAPIView.as_view()),
    path('colors/create/', ColorCreateAPIView.as_view()),
    path('colors/<uuid:color_id>/', ColorDetailAPIView.as_view()),
    path('colors/<uuid:color_id>/update/', ColorUpdateAPIView.as_view()),
    path('colors/<uuid:color_id>/delete/', ColorDeleteAPIView.as_view()),

    # SIZES
    path('sizes/', SizeListAPIView.as_view()),
    path('sizes/create/', SizeCreateAPIView.as_view()),
    path('sizes/<uuid:size_id>/', SizeDetailAPIView.as_view()),
    path('sizes/<uuid:size_id>/update/', SizeUpdateAPIView.as_view()),
    path('sizes/<uuid:size_id>/delete/', SizeDeleteAPIView.as_view()),

     # ================= PRODUCT =================
    path("products/", ProductListAPIView.as_view()),
    path("products/create/", ProductCreateAPIView.as_view()),
    path("products/<uuid:product_id>/", ProductDetailAPIView.as_view()),
    path("products/<uuid:product_id>/update/", ProductUpdateAPIView.as_view()),
    path("products/<uuid:product_id>/delete/", ProductDeleteAPIView.as_view()),

    path("products/full-create/", ProductFullCreateAPIView.as_view()),



    # ================= INVENTORY =================
    path("inventory/", ProductInventoryListAPIView.as_view()),
    path("inventory/create/", ProductInventoryCreateAPIView.as_view()),
    path("inventory/<uuid:inventory_id>/", ProductInventoryDetailAPIView.as_view()),
    path("inventory/<uuid:inventory_id>/update/", ProductInventoryUpdateAPIView.as_view()),
    path("inventory/<uuid:inventory_id>/delete/", ProductInventoryDeleteAPIView.as_view()),


    # ================= PRODUCT IMAGES =================
    path("products/<uuid:product_id>/images/", ProductImageListAPIView.as_view()),
    path("products/images/create/", ProductImageCreateAPIView.as_view()),
    path("products/images/<uuid:image_id>/update/", ProductImageUpdateAPIView.as_view()),
    path("products/images/<uuid:image_id>/delete/", ProductImageDeleteAPIView.as_view()),

    # Admin
    path("admin/orders/<uuid:order_id>/cancel/",CancelOrderAPIView.as_view(),name="admin-cancel-order"),

    # Admin / Ops – Mark RTO
    path("admin/orders/<uuid:order_id>/rto/",MarkOrderRTOAPIView.as_view(),name="admin-mark-rto"),

    # Orders
    path("admin/orders/", AdminOrderListAPIView.as_view()),
    path("admin/orders/stats/", AdminOrderStatsAPIView.as_view()),
    path("admin/orders/<uuid:order_id>/", AdminOrderDetailAPIView.as_view()),
    path("admin/orders/<uuid:order_id>/status/", AdminUpdateOrderStatusAPIView.as_view()),

    # 🛒 CART APIs
    path("cart/add/", AddToCartAPIView.as_view(), name="add-to-cart"),
    path("cart/", ViewCartAPIView.as_view(), name="view-cart"),
    path("cart/item/<uuid:item_id>/update/", UpdateCartItemAPIView.as_view(), name="update-cart-item"),
    path("cart/item/<uuid:item_id>/delete/", RemoveCartItemAPIView.as_view(), name="remove-cart-item"),

    # 📦 ORDER API
    path("order/place/", PlaceOrderAPIView.as_view(), name="place-order"),
]
