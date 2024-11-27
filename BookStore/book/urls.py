from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, SubCategoryViewSet, ImportProductsView ,ProductSearchView,advanced_search

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('import-products/', ImportProductsView.as_view(), name='import-products'),
    path('search/', ProductSearchView.as_view(), name='product-search'),
    path('advanced-search/', advanced_search, name='advanced_search'),
]
