from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, RoleViewSet , AuthToken , ProtectedAPI
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'roles', RoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', AuthToken.as_view(), name='token_obtain'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedAPI.as_view(), name='protected-api'),
   
]
