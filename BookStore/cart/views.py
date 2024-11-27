from rest_framework import viewsets
from .models import Order, OrderDetail, Cart , Voucher , CartItem
from .serializers import OrderSerializer, OrderDetailSerializer, CartSerializer, VoucherSerializer , CartItemSerializer
from rest_framework.permissions import IsAuthenticated
from book.models import Product
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction
import uuid
import requests
import hmac
import hashlib
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    @action(detail=False, methods=['get'], url_path='by-order')
    def by_order(self, request):
        # Lấy order_id từ query params
        order_id = request.query_params.get('order_id')
        if not order_id:
            return Response({"error": "order_id is required."}, status=400)

        # Kiểm tra nếu Order tồn tại và chưa bị xóa
        order = Order.objects.filter(id=order_id, isDelete=False).first()
        if not order:
            raise NotFound({"error": f"Order with id {order_id} not found or has been deleted."})

        # Lọc OrderDetail theo order_id và kiểm tra trạng thái isDelete
        order_details = self.queryset.filter(order_id=order_id, isDelete=False)
        if not order_details.exists():
            raise NotFound({"error": f"No order details found for order_id {order_id}."})

        # Serialize dữ liệu nếu tồn tại
        serializer = self.get_serializer(order_details, many=True)
        return Response(serializer.data)

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

        # Lấy phí vận chuyển từ request
        shipping = request.data.get('shipping', 0)
        amount = cart.total + shipping  # Tổng tiền cần thanh toán

        # Thông tin MoMo
        endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
        accessKey = "F8BBA842ECF85"
        secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
        
        partnerCode = "MOMO"
        redirectUrl = "https://bk-bookstore.vercel.app/"
        ipnUrl = redirectUrl
        extraData = ""
        partnerName = "Bookstore"
        requestType = "payWithMethod"
        storeId = "Test Store"
        lang = "vi"

        # Tạo ID đơn hàng và request
        order_id = str(uuid.uuid4())
        request_id = str(uuid.uuid4())
        orderInfo = f"Thanh toán đơn hàng {order_id}tại Bookstore, tổng cộng {amount} VNĐ"
        # Tạo chữ ký
        rawSignature = (
            f"accessKey={accessKey}&amount={amount}&extraData={extraData}&ipnUrl={ipnUrl}"
            f"&orderId={order_id}&orderInfo={orderInfo}&partnerCode={partnerCode}"
            f"&redirectUrl={redirectUrl}&requestId={request_id}&requestType={requestType}"
        )
        h = hmac.new(bytes(secretKey, 'utf-8'), bytes(rawSignature, 'utf-8'), hashlib.sha256)
        signature = h.hexdigest()

       
        data = {
            'partnerCode': partnerCode,
            'orderId': order_id,
            'partnerName': partnerName,
            'storeId': storeId,
            'ipnUrl': ipnUrl,
            'amount': str(amount),  
            'lang': lang,
            'requestType': requestType,
            'redirectUrl': redirectUrl,
            'autoCapture': True,
            'orderInfo': orderInfo,
            'requestId': request_id,
            'extraData': extraData,
            'signature': signature,
            'orderGroupId': ""
        }

        response = requests.post(endpoint, json=data, headers={'Content-Type': 'application/json'})
       

        if response.status_code == 200:
            response_data = response.json()
            with transaction.atomic():
                        # Tạo Order
                        order = Order.objects.create(
                            user=request.user,
                            discount=cart.discount,
                            sub_total=cart.sub_total,
                            total=amount,
                            shipping=shipping,
                        )

                        # Tạo OrderDetail cho từng CartItem
                        for cart_item in cart.cart_items.filter(is_delete=False):
                            OrderDetail.objects.create(
                                order=order,
                                product=cart_item.product,
                                quantity=cart_item.quantity,
                                total=cart_item.total,
                                discount=cart_item.product.discount if hasattr(cart_item.product, 'discount') else 0,
                            )
                            # Đánh dấu CartItem là đã xóa
                            cart_item.is_delete = True
                            cart_item.save()

                        # Tính toán lại tổng giỏ hàng
                        cart.calculate_totals()

            return Response({
                "message": "Checkout thành công.",
                "order_id": order.id,
                "payUrl": response_data.get('shortLink')
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Không thể kết nối đến MoMo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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



