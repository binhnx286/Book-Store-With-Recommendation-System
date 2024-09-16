from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, RoleViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'roles', RoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
