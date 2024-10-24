from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderDetailViewSet, CartViewSet, VoucherViewSet ,CartItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order-details', OrderDetailViewSet)
router.register(r'carts', CartViewSet)
router.register(r'vouchers', VoucherViewSet)
router.register(r'cart-items', CartItemViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
