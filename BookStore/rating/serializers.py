from rest_framework import serializers
from .models import Rating
from user.serializers import AccountSerializer

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField() 
    class Meta:
        model =  Rating
        fields = ['id','user','product','rate','feed_back','isDelete']
    def get_user(self, obj):
        # Sử dụng AccountSerializer để serialize user và chỉ lấy tên
        return {"name": obj.user.name,
                "email":obj.user.email}