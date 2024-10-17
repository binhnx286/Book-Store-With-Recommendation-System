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
from django.db.models import Avg
from rest_framework.decorators import action


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.request.data.get('user')  # Lấy user_id từ request
    
        try:
            user = Account.objects.get(id=user_id)  # Lấy người dùng từ cơ sở dữ liệu
        except Account.DoesNotExist:
            raise ValidationError({"user": "Người dùng không tồn tại."})

        serializer.save(user=user)  # Gán người dùng cho đối tượng Rating
    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        """Trả về trung bình rating và danh sách các đánh giá cho một sản phẩm."""
        product_id = pk  # Lấy product_id từ URL

        # Tính trung bình rating cho sản phẩm có id = product_id
        average = Rating.objects.filter(product_id=product_id).aggregate(Avg('rate'))['rate__avg']

        # Nếu không có đánh giá, thiết lập giá trị mặc định cho average
        if average is None:
            average = 0

        # Lấy tất cả các đánh giá cho sản phẩm
        ratings = Rating.objects.filter(product_id=product_id, isDelete=False)
        
        # Sử dụng RatingSerializer để serialize danh sách các đánh giá
        serializer = RatingSerializer(ratings, many=True)

        # Trả về kết quả gồm trung bình rating và danh sách đánh giá
        return Response({
            "product_id": product_id,
            "average_rating": average,
            "ratings": serializer.data  # Danh sách các đánh giá bao gồm thông tin người dùng
        }, status=status.HTTP_200_OK)
    
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
        recommendations = [rec for rec in recommendations if rec[0] != user_id]
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

        similarity_threshold = 0.6  
        if not recommendations or 'U' in [rec[0] for rec in recommendations]:
            return Response({'message': 'No recommendations available or invalid recommendations for this user'}, status=status.HTTP_200_OK)
        else:
            filtered_recommendations = [
                rec for rec in recommendations if rec[1] >= similarity_threshold
            ]
            
            print(filtered_recommendations)
            num_recommendations = int(request.query_params.get('num', 5))
            filtered_recommendations = filtered_recommendations[:num_recommendations]

        

            recommended_product_ids = []
            for rec in filtered_recommendations:
                user = rec[0]
                user_high_ratings = Rating.objects.filter(user_id=user, rate__gte=4).values_list('product_id', flat=True)
                recommended_product_ids.extend(user_high_ratings)
            user_rated_products = Rating.objects.filter(user_id=user_id).values_list('product_id', flat=True)
            recommended_product_ids = list(set(recommended_product_ids) - set(user_rated_products))

            # Lấy các sản phẩm tương ứng với ID
            recommended_products = Product.objects.filter(id__in=recommended_product_ids)

            # Sử dụng serializer để chuyển đổi danh sách sản phẩm thành JSON
            serializer = ProductSerializer(recommended_products, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)