from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, RoleViewSet , AuthToken , ProtectedAPI, PasswordResetView, CheckPasswordView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'roles', RoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('check-password/', CheckPasswordView.as_view(), name='check_password'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('login/', AuthToken.as_view(), name='token_obtain'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('protected/', ProtectedAPI.as_view(), name='protected-api'),
   
]
