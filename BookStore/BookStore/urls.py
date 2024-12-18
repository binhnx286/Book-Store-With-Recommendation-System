"""
URL configuration for BookStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.http import HttpResponse

from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

def home(request):
    
    return HttpResponse("Welcome to the Django application!")

urlpatterns = [
    path('', home),
    path('grappelli/', include('grappelli.urls')),
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls")),
    path("api/book/", include("book.urls")),
    path('api/rating/', include('rating.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/promotion/', include('promotion.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')), 
    #json
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # ReDoc UI
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
