from rest_framework import viewsets
from .models import Order, OrderDetail, Cart , Voucher , CartItem
from .serializers import OrderSerializer, OrderDetailSerializer, CartSerializer, VoucherSerializer , CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from book.models import Product
from rest_framework.response import Response
from rest_framework import status

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).prefetch_related('cart_items')

    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        # Kiểm tra số lượng hợp lệ
        if quantity <= 0:
            return Response({"error": "Số lượng phải lớn hơn 0."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Sản phẩm không tồn tại."}, status=status.HTTP_404_NOT_FOUND)

        if quantity > product.quantity:
            return Response({
                "error": f"Số lượng yêu cầu vượt quá tồn kho. Chỉ còn {product.quantity} sản phẩm trong kho."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Lấy hoặc tạo giỏ hàng cho người dùng
        cart, created = Cart.objects.get_or_create(user=request.user, defaults={'discount': 0, 'sub_total': 0, 'total': 0})

        # Lấy hoặc tạo CartItem cho sản phẩm
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Cập nhật số lượng và tổng
        cart_item.quantity += quantity
        cart_item.save()  # Lưu CartItem

        product.quantity -= quantity
        product.save()  # Lưu sản phẩm sau khi cập nhật tồn kho

        # # Cập nhật tổng giá trị của giỏ hàng
        # cart.calculate_totals()  # Tính toán lại tổng cho giỏ hàng

        # Tạo dữ liệu trả về
        response_data = {
            "product_id": product.id,
            "product_name": product.name,
            "quantity": cart_item.quantity,
            "total_price": cart_item.total,  # Sử dụng tổng của CartItem
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart_id = self.request.query_params.get('cart_id')  
        if cart_id:
            return self.queryset.filter(cart_id=cart_id) 
        return self.queryset  
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        quantity = request.data.get('quantity', instance.quantity)

        # Cập nhật số lượng
        if quantity < 0:
            return Response({"error": "Số lượng không được nhỏ hơn 0."}, status=status.HTTP_400_BAD_REQUEST)

        # Tính toán lại số lượng nếu số lượng đã thay đổi
        if quantity != instance.quantity:
            # Lưu số lượng hiện tại để trả lại vào kho nếu cần
            quantity_difference = quantity - instance.quantity

            # Cập nhật số lượng trong CartItem
            instance.quantity = quantity
            instance.save()

            # Cập nhật số lượng của sản phẩm
            product = instance.product
            product.quantity -= quantity_difference
            product.save()  # Lưu lại sản phẩm

        # Tính lại tổng cho CartItem
        instance.save()  # Lưu lại tổng giá trị của CartItem

        # Tính toán lại tổng cho giỏ hàng
        instance.cart.calculate_totals()

        # Trả về dữ liệu đã cập nhật
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  
        cart = instance.cart  

        # Lưu số lượng sản phẩm để tăng lại vào kho
        quantity_to_return = instance.quantity

        # Gọi phương thức để xóa CartItem
        self.perform_destroy(instance)

        # Tăng lại số lượng vào kho
        product = instance.product
        product.quantity += quantity_to_return
        product.save()  # Lưu lại sản phẩm

        # Tính toán lại tổng cho giỏ hàng
        cart.calculate_totals() 

        return Response(status=status.HTTP_204_NO_CONTENT)
        
class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer



