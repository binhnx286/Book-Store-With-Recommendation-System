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
    # Sử dụng PrimaryKeyRelatedField để liên kết với Rating và Account (user) bằng ID
    rating = serializers.PrimaryKeyRelatedField(queryset=Rating.objects.all())  # Nhận ID của Rating
    user = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())  # Nhận ID của User
    
    response_text = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = RatingResponse
        fields = ['rating', 'user', 'response_text', 'created_at']