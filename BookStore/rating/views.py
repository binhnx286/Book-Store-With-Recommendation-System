from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Rating
from .serializers import RatingSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.filter(isDelete=False)  
    serializer_class = RatingSerializer
    # permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 

