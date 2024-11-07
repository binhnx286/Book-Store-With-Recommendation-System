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
        """Chỉ trả về các khuyến mãi đang hoạt động nếu có yêu cầu đặc biệt."""
        active_only = self.request.query_params.get('active_only', None)
        queryset = self.queryset
        if active_only == 'true':
            queryset = queryset.filter(
                is_active=True,
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            )
        return queryset
