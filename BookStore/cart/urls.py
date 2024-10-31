from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderDetailViewSet, CartViewSet, VoucherViewSet ,CartItemViewSet ,CheckoutView

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order-details', OrderDetailViewSet)
router.register(r'carts', CartViewSet)
router.register(r'vouchers', VoucherViewSet)
router.register(r'cart-items', CartItemViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('checkout/', CheckoutView.as_view(), name='cart-checkout'),
    path('checkout/<int:order_id>/', CheckoutView.as_view(), name='cart-checkout'),
]
