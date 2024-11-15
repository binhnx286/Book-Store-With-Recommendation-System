from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RatingViewSet,BookRecommendationAPIView,BookRecommendationListAPIView,RatingResponseViewSet

router = DefaultRouter()
router.register(r'ratings', RatingViewSet)
# router.register(r'rating-responses', RatingResponseViewSet)
urlpatterns = [
    path('', include(router.urls)),
     path('rating-responses/<int:rating_id>/', RatingResponseViewSet.as_view({'get': 'list', 'post': 'create'}), name='rating-responses'),
    path('recommendations/<int:user_id>/', BookRecommendationAPIView.as_view(), name='book-recommendations'),
    path('recommendations-list/<int:user_id>/', BookRecommendationListAPIView.as_view(), name='book-recommendations-list'),
    
    
]
