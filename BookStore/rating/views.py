from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Rating
from .serializers import RatingSerializer

from rest_framework.views import APIView
from .knn import kNNCollaborativeFiltering
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from user.models import Account
from book.serializers import ProductSerializer
from book.models import Product


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.request.data.get('user')  # Lấy user_id từ request
    
        try:
            user = Account.objects.get(id=user_id)  # Lấy người dùng từ cơ sở dữ liệu
        except Account.DoesNotExist:
            raise ValidationError({"user": "Người dùng không tồn tại."})

        serializer.save(user=user)  # Gán người dùng cho đối tượng Rating

class BookRecommendationListAPIView(APIView):
    def get(self, request, user_id):
        # Lấy ma trận người dùng - sản phẩm
        X_train = kNNCollaborativeFiltering.get_user_product_matrix()
        
        # Khởi tạo mô hình với số hàng xóm k = 5
        model = kNNCollaborativeFiltering(k_neighbours=5)
        
        # Huấn luyện mô hình
        model.fit(X_train)
        
        # Dự đoán gợi ý cho người dùng
        recommendations = model.predict(user_id)
        
        # Chuyển đổi gợi ý thành định dạng JSON
        recommendation_list = [
            {
                'user_id': rec[0],
                'similarity_score': rec[1]
            } for rec in recommendations
        ]
        
        return Response(recommendation_list, status=status.HTTP_200_OK)
    
class BookRecommendationAPIView(APIView):
    def get(self, request, user_id):
        # Kiểm tra người dùng có tồn tại không
        if not Account.objects.filter(id=user_id).exists():
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Lấy ma trận người dùng - sản phẩm
        X_train = kNNCollaborativeFiltering.get_user_product_matrix()
        
        # k = 5
        model = kNNCollaborativeFiltering(k_neighbours=5)
        
        # Huấn luyện mô hình
        model.fit(X_train)
        
        # Dự đoán gợi ý cho người dùng
        recommendations = model.predict(user_id)
        
        if not recommendations or 'U' in [rec[0] for rec in recommendations]:
            return Response({'message': 'No recommendations available or invalid recommendations for this user'}, status=status.HTTP_200_OK)

        # Chuyển đổi gợi ý thành danh sách sản phẩm được gợi ý
        recommended_product_ids = [rec[0] for rec in recommendations]  # Lấy danh sách ID sản phẩm

        # Lấy các sản phẩm tương ứng với ID
        recommended_products = Product.objects.filter(id__in=recommended_product_ids)

        # Sử dụng serializer để chuyển đổi danh sách sản phẩm thành JSON
        serializer = ProductSerializer(recommended_products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)