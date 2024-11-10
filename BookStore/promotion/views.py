from rest_framework import viewsets
from .models import Promotion
from .serializers import PromotionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone

class PromotionViewSet(viewsets.ReadOnlyModelViewSet):
    """API cho Promotion, chỉ cho phép xem"""
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    

    def get_queryset(self):
        """Trả về các khuyến mãi đang hoạt động, bao gồm cả khi có cập nhật."""
        queryset = Promotion.objects.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
        return queryset