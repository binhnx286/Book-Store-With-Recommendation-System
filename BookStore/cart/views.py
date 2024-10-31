from rest_framework import viewsets
from .models import Order, OrderDetail, Cart , Voucher , CartItem
from .serializers import OrderSerializer, OrderDetailSerializer, CartSerializer, VoucherSerializer , CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from book.models import Product
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
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

       
        cart_item = CartItem.objects.filter(cart=cart, product=product, is_delete=False).first()

        if cart_item:
            # Nếu tồn tại, cập nhật số lượng
            cart_item.quantity += quantity
            cart_item.save()  # Lưu CartItem
        else:
            # Nếu không tồn tại, tạo mới CartItem
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        product.quantity -= quantity
        product.save()  
       
        # Tạo dữ liệu trả về
        response_data = {
            "product_id": product.id,
            "product_name": product.name,
            "quantity": cart_item.quantity,
            "total_price": cart_item.total,  # Sử dụng tổng của CartItem
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            # Lấy đơn hàng theo order_id
            order = Order.objects.get(id=order_id)

            # Lấy tất cả OrderDetail liên quan đến order
            order_details = OrderDetail.objects.filter(order=order)

            # Serialize dữ liệu
            serializer = OrderDetailSerializer(order_details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        # Lấy giỏ hàng của người dùng
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.cart_items.filter(is_delete=False).exists():
            return Response({"error": "Giỏ hàng trống."}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy phí vận chuyển từ request, nếu không có thì sử dụng giá trị mặc định
        shipping = request.data.get('shipping', 0)  # Ví dụ: giá trị mặc định là 0

        # Tạo Order
        order = Order.objects.create(
            user=request.user,
            discount=cart.discount,
            sub_total=cart.sub_total,
            total=cart.total + shipping,  # Thêm chi phí vận chuyển vào tổng
            shipping=shipping,  # Lưu phí vận chuyển
        )

        # Tạo OrderDetail cho mỗi CartItem
        for cart_item in cart.cart_items.filter(is_delete=False):
            OrderDetail.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                total=cart_item.total,
                discount=cart_item.product.discount if hasattr(cart_item.product, 'discount') else 0,  # Lưu giảm giá nếu có
            )
            # Đánh dấu CartItem là đã xóa
            cart_item.is_delete = True
            cart_item.save()

        # Tính toán lại tổng giỏ hàng
        cart.calculate_totals()

        return Response({"message": "Checkout thành công.", "order_id": order.id}, status=status.HTTP_201_CREATED)


    

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart_id = self.request.query_params.get('cart_id')  
        if cart_id:
            # Chỉ lấy các CartItem chưa bị xóa (is_delete=False)
            return self.queryset.filter(cart_id=cart_id, is_delete=False) 
        # Trả về tất cả CartItem chưa bị xóa
        return self.queryset.filter(is_delete=False) 
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



