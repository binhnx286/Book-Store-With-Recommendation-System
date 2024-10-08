from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RatingViewSet,BookRecommendationAPIView,BookRecommendationListAPIView

router = DefaultRouter()
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recommendations/<int:user_id>/', BookRecommendationAPIView.as_view(), name='book-recommendations'),
    path('recommendations-list/<int:user_id>/', BookRecommendationListAPIView.as_view(), name='book-recommendations-list'),
    
]
