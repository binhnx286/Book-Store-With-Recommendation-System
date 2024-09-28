from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderDetailViewSet, CartViewSet, VoucherViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order-details', OrderDetailViewSet)
router.register(r'carts', CartViewSet)
router.register(r'vouchers', VoucherViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
