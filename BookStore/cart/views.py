from rest_framework import viewsets, status
from .models import Order, OrderDetail, Cart , Voucher
from .serializers import OrderSerializer, OrderDetailSerializer, CartSerializer, VoucherSerializer
from rest_framework.response import Response


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     user = request.user

    #     # Nhận sub_total từ request
    #     sub_total = data.get('sub_total')
    #     voucher_code = data.get('voucher', None)  # Voucher có thể không có

    #     discount = 0  # Mặc định không có giảm giá
    #     if voucher_code:
    #         try:
    #             voucher = Voucher.objects.get(id=voucher_code, isDelete=False)
    #             discount = (voucher.discount_percent / 100) * sub_total  # Tính phần trăm giảm giá
    #         except Voucher.DoesNotExist:
    #             return Response({"detail": "Invalid voucher code."}, status=status.HTTP_400_BAD_REQUEST)

    #     # Tính tổng tiền sau khi áp dụng giảm giá (nếu có)
    #     total = sub_total - discount

    #     # Tạo đơn hàng
    #     order = Order.objects.create(
    #         user=user,
    #         sub_total=sub_total,
    #         total=total,
    #         discount=discount,
    #         shipping=data.get('shipping', 0),  # Mặc định phí vận chuyển = 0 nếu không có
    #         status="Pending"
    #     )

    #     # Trả về dữ liệu của đơn hàng mới tạo
    #     return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer

