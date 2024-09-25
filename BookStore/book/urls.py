from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, BrandViewSet, CategoryViewSet, SubCategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
