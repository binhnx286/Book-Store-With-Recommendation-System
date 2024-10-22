from rest_framework import viewsets
from .models import Order, OrderDetail, Cart , Voucher
from .serializers import OrderSerializer, OrderDetailSerializer, CartSerializer, VoucherSerializer
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
        # Chỉ trả về giỏ hàng của người dùng đã đăng nhập
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        print("Create method called.")
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

        
        print(f"Creating cart for user {request.user.id}, product_id: {product_id}, quantity: {quantity}, price: {product.new_price}")

        total_price = quantity * int( product.new_price.replace('.', ''))
        print(total_price)
        
        
        return Response(status=status.HTTP_201_CREATED)
    
class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer



