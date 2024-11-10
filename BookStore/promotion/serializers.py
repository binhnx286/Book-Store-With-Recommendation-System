from rest_framework import serializers
from .models import Promotion
import re
from book.serializers import ProductSerializer, SubCategorySerializer

class PromotionSerializer(serializers.ModelSerializer):
    

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
            'is_active',
            'promotion_type',
            'products',
            'subcategories'
        ]

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
        return representation
