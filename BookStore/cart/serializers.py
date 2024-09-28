from rest_framework import serializers
from .models import Order, OrderDetail, Cart , Voucher

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'

# class OrderSerializer(serializers.ModelSerializer):
#     voucher = serializers.IntegerField(write_only=True, required=False)  # ID voucher từ client

#     class Meta:
#         model = Order
#         fields = '__all__'

#     def create(self, validated_data):
#         voucher_id = validated_data.pop('voucher', None)  # Lấy voucher nếu có
#         sub_total = validated_data.get('sub_total', 0)
#         discount = 0

#         # Nếu có voucher, áp dụng giảm giá
#         if voucher_id:
#             try:
#                 voucher = Voucher.objects.get(id=voucher_id, isDelete=False)
#                 discount = (voucher.discount_percent / 100) * sub_total
#             except Voucher.DoesNotExist:
#                 raise serializers.ValidationError({"voucher": "Voucher không hợp lệ."})

#         # Tính total sau khi áp dụng discount
#         validated_data['discount'] = discount
#         validated_data['total'] = sub_total - discount

#         # Tạo order
#         return super().create(validated_data)
