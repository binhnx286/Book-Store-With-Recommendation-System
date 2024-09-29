from rest_framework import viewsets
from .models import Product, Category, SubCategory
from .serializers import ProductSerializer, CategorySerializer, SubCategorySerializer

import csv
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category', None)
        subcategory_id = self.request.query_params.get('subcategory', None)

        if category_id is not None:
             queryset = queryset.filter(sub_category__category__id=category_id)

        if subcategory_id is not None:
            queryset = queryset.filter(sub_category_id=subcategory_id)

        return queryset
def import_products_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                sub_category = SubCategory.objects.get(id=row['sub_category'])

                product = Product(
                    name=row['name'].strip(),
                    description=row['description'],
                    image=row['image'],
                    quantity=int(row['quantity']),
                    price_origin=float(row['price_origin']),
                    new_price=float(row['new_price']) if row['new_price'] else None,
                    viewed=int(row['view']),
                    sub_category=sub_category,
                )
                product.save()
            except ObjectDoesNotExist:
                print(f"SubCategory not found for row: {row}")
            except Exception as e:
                print(f"Error importing row {row}: {e}")

class ImportProductsView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file.name.endswith('.csv'):
            return Response({"detail": "File must be a CSV."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Lưu file tạm thời
        upload_dir = 'uploads'  # Thay đổi đường dẫn theo ý muốn
        os.makedirs(upload_dir, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại
        file_path = os.path.join(upload_dir, file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        failed_rows = import_products_from_csv(file_path)

        # Xóa file tạm thời nếu không cần thiết
        os.remove(file_path)

        if failed_rows:
            return Response({
                "detail": "Products imported with some errors.",
                "failed_rows": failed_rows  # Trả về danh sách các dòng không thành công
            }, status=status.HTTP_206_PARTIAL_CONTENT)

        return Response({"detail": "Products imported successfully."}, status=status.HTTP_201_CREATED)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


