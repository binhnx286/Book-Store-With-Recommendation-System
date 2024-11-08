from rest_framework import serializers
from .models import Promotion
import re
from book.serializers import ProductSerializer, SubCategorySerializer

class PromotionSerializer(serializers.ModelSerializer):
    is_active_promotion = serializers.SerializerMethodField()

    products = ProductSerializer(many=True, read_only=True)
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Promotion
        fields = [
            'id',
            'name',
            'description',
            'discount_percent',
            'start_date',
            'end_date',
            'is_active_promotion',
            'promotion_type',
            'products',
            'subcategories'
        ]
    
    def get_is_active_promotion(self, obj):
        """Trả về True nếu khuyến mãi đang hoạt động."""
        return obj.is_active_promotion()
    def to_representation(self, instance):
        """Override to_representation để chỉnh sửa link ảnh trong description."""
        representation = super().to_representation(instance)
        
        # Lấy dữ liệu description và thêm tiền tố vào các URL ảnh
        description = representation.get('description', '')
        
        # Thêm tiền tố URL cho các ảnh trong description
        if description:
            # Sử dụng regex để tìm các src="..." và thêm tiền tố vào
            description = re.sub(r'src="(/media/[^"]+)"', r'src="https://bk-bookstore.azurewebsites.net\1"', description)
        
        # Cập nhật lại description sau khi thay đổi
        representation['description'] = description
        print(representation)
        return representation