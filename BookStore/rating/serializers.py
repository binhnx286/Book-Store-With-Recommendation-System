from rest_framework import serializers
from .models import Rating,RatingResponse
from user.serializers import AccountSerializer
from user.models import Account

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField() 
    class Meta:
        model =  Rating
        fields = ['id','user','product','rate','feed_back','isDelete']
    def get_user(self, obj):
        # Sử dụng AccountSerializer để serialize user và chỉ lấy tên
        return {"name": obj.user.username,
                "email":obj.user.email}
    


class RatingResponseSerializer(serializers.ModelSerializer):
    # Nhúng thông tin email người phản hồi
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = RatingResponse
        fields = ['rating', 'user_email', 'response_text', 'created_at']
        read_only_fields = ['user']  
    
    def validate(self, attrs):
        # Kiểm tra nếu đánh giá đã bị tắt (is_disabled = True)
        rating = attrs.get('rating')
        if rating.is_disabled:
            raise serializers.ValidationError("Không thể phản hồi cho đánh giá này vì nó đã bị tắt.")
        return attrs
