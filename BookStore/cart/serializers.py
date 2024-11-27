from rest_framework import serializers
from .models import Order, OrderDetail, Cart , Voucher , CartItem
from book.models import Product

class OrderSerializer(serializers.ModelSerializer):
    voucher = serializers.IntegerField(write_only=True, required=False)  # ID voucher từ client
    order_details = serializers.ListField(write_only=True)  # Danh sách chi tiết đơn hàng từ client

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, data):
        order_details = data.get('order_details', [])

        for detail in order_details:
            product_id = detail.get('product_id')
            quantity = detail.get('quantity')

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError({"product_id": "Sản phẩm không tồn tại."})

            if quantity > product.stock:
                raise serializers.ValidationError({
                    "quantity": f"Số lượng yêu cầu vượt quá tồn kho. Chỉ còn {product.stock} sản phẩm trong kho."
                })

        return data

    def create(self, validated_data):
        voucher_id = validated_data.pop('voucher', None)
        order_details = validated_data.pop('order_details', [])
        sub_total = sum(detail['quantity'] * Product.objects.get(id=detail['product_id']).price for detail in order_details)
        discount = 0

        # Áp dụng voucher nếu có
        if voucher_id:
            try:
                voucher = Voucher.objects.get(id=voucher_id, isDelete=False)
                discount = (voucher.discount_percent / 100) * sub_total
            except Voucher.DoesNotExist:
                raise serializers.ValidationError({"voucher": "Voucher không hợp lệ."})

        validated_data['sub_total'] = sub_total
        validated_data['discount'] = discount
        validated_data['total'] = sub_total - discount + validated_data.get('shipping', 0)

        # Tạo order
        order = super().create(validated_data)

      
        for detail in order_details:
            product = Product.objects.get(id=detail['product_id'])
            if detail['quantity'] > product.stock:
                raise serializers.ValidationError({
                    "quantity": f"Số lượng yêu cầu vượt quá tồn kho. Chỉ còn {product.stock} sản phẩm trong kho."
                })

            # Tạo OrderDetail
            OrderDetail.objects.create(
                order=order,
                product=product,
                quantity=detail['quantity'],
                total=product.price * detail['quantity'],
                discount=0  # Cập nhật discount nếu cần thiết
            )

            # Cập nhật số lượng tồn kho của sản phẩm
            product.stock -= detail['quantity']
            product.save()

        return order

class OrderDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()  
    image = serializers.SerializerMethodField()
    class Meta:
        model = OrderDetail
        fields = ['id', 'order', 'product', 'product_name','image','quantity', 'total']
    def get_product_name(self, obj):
        return obj.product.name  
    def get_image(self, obj):
            return obj.product.image
class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()  

    class Meta:
        model = CartItem
        fields = ['id','product', 'product_name', 'quantity', 'total']  

    def get_product_name(self, obj):
        return obj.product.name  

class CartSerializer(serializers.ModelSerializer):
    
    cart_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'discount', 'sub_total', 'total', 'user', 'cart_items']

    def get_cart_items(self, obj):
        # Lọc cart_items để chỉ lấy những cái không bị xóa
        return CartItemSerializer(obj.cart_items.filter(is_delete=False), many=True).data

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = '__all__'

