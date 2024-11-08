from rest_framework import serializers
from .models import Promotion

class PromotionSerializer(serializers.ModelSerializer):
    is_active_promotion = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = ['id', 'name', 'description', 'discount_percent', 'start_date', 'end_date', 'is_active', 'is_active_promotion', 'promotion_type']
    
    def get_is_active_promotion(self, obj):
        """Trả về True nếu khuyến mãi đang hoạt động."""
        return obj.is_active_promotion()
    