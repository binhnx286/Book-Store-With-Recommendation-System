from rest_framework import viewsets
from .models import Product, Category, SubCategory
from .serializers import ProductSerializer, CategorySerializer, SubCategorySerializer

import csv
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import re
from django.db.models import Q
from rest_framework.decorators import action

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
    @action(detail=False, methods=['get'], url_path='highest-discount')
    def highest_discount(self, request):
        # Sắp xếp sản phẩm theo discount_percent (từ cao đến thấp)
        products_with_discount = sorted(
            Product.objects.all(),
            key=lambda product: product.discount_percent,
            reverse=True
        )
        
        if not products_with_discount:
            return Response({"detail": "Không có sản phẩm nào có mức giảm giá."}, status=status.HTTP_404_NOT_FOUND)
        
        
        highest_discount_product = products_with_discount[0]
        serializer = self.get_serializer(highest_discount_product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductSearchView(APIView):
    def get(self, request, *args, **kwargs):
        name = request.query_params.get('name', None)
        publishers = request.query_params.getlist('publisher', None)
        authors = request.query_params.get('author', None)
        publication_years = request.query_params.get('publication_years', None) 
        sub_categories = request.query_params.getlist('sub_category', None)

        queryset = Product.objects.all()
        query_conditions = Q()  # Khởi tạo điều kiện tìm kiếm

        # Tìm kiếm theo name
        if name:
            if re.match(r'^".*"$', name):  
                name = name[1:-1]
                query_conditions &= Q(name__iexact=name)  
            else:  
                query_conditions &= Q(name__icontains=name)

        # Tìm kiếm theo publisher
        if publishers:
            publisher_conditions = Q()  # Khởi tạo điều kiện cho publisher
            for p in publishers:
                if re.match(r'^".*"$', p): 
                    p = p[1:-1]
                    publisher_conditions |= Q(publisher__iexact=p)  
                else:  
                    publisher_conditions |= Q(publisher__icontains=p)

            query_conditions &= publisher_conditions  # Kết hợp với điều kiện chính

        # Tìm kiếm theo author
        if authors:
            author_conditions = Q()  # Khởi tạo điều kiện cho author
            authors_list = authors.split('|')  # Tách các tác giả bằng '|'
            for a in authors_list:
                if re.match(r'^".*"$', a):  
                    a = a[1:-1]
                    author_conditions |= Q(author__iexact=a)  
                else:  
                    author_conditions |= Q(author__icontains=a)

            query_conditions &= author_conditions  # Kết hợp với điều kiện chính

        # Tìm kiếm theo publication_year
        if publication_years:
            # Tách các giá trị năm bằng ký tự '|'
            years_list = publication_years.split('|')
            year_filters = Q()  # Khởi tạo điều kiện tìm kiếm cho năm
            for y in years_list:
                if re.match(r'^".*"$', y):  
                    y = y[1:-1]
                    year_filters |= Q(publication_year__iexact=y)  # Thêm điều kiện OR
                else:  
                    year_filters |= Q(publication_year__iexact=y)

            query_conditions &= year_filters  # Kết hợp với điều kiện chính

        # Tìm kiếm theo sub_category
        if sub_categories:
            sub_category_conditions = Q()  # Khởi tạo điều kiện cho sub_category
            for sc in sub_categories:
                if re.match(r'^".*"$', sc): 
                    sc = sc[1:-1]
                    sub_category_conditions |= Q(sub_category__name__iexact=sc) 
                else:  
                    sub_category_conditions |= Q(sub_category__name__icontains=sc)

            query_conditions &= sub_category_conditions  # Kết hợp với điều kiện chính

        # Áp dụng tất cả các điều kiện tìm kiếm
        queryset = queryset.filter(query_conditions)

        # Lấy các giá trị duy nhất cho các trường
        filtered_sub_categories = queryset.values_list('sub_category__name', flat=True).distinct()
        filtered_publishers = queryset.values_list('publisher', flat=True).distinct()
        filtered_authors = queryset.values_list('author', flat=True).distinct()
        filtered_publication_years = queryset.values_list('publication_year', flat=True).distinct()

        # Serialize kết quả
        serializer = ProductSerializer(queryset, many=True)

        if not queryset.exists():
            return Response({"message": "Không tìm thấy sản phẩm phù hợp."}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "products": serializer.data,
            "sub_categories": list(filtered_sub_categories),
            "publishers": list(filtered_publishers),
            "authors": list(filtered_authors),
            "publication_years": list(filtered_publication_years)  
        }, status=status.HTTP_200_OK)
    
def import_products_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                sub_category = SubCategory.objects.get(id=row['sub_category'])

                # product = Product(
                #     name=row['name'].strip(),
                #     description=row['description'],
                #     image=row['image'],
                #     quantity=int(row['quantity']),
                #     price_origin=float(row['price_origin']),
                #     new_price=float(row['new_price']) if row['new_price'] else None,
                #     viewed=int(row['view']),
                #     sub_category=sub_category,
                # )
                product = Product(
                    name=row['name'].strip(),
                    description=row['description'],
                    image=row['image'],
                    quantity=int(row['quantity']),
                    price_origin=row['price_origin'],  # Giữ nguyên như CharField
                    new_price=row['new_price'] if row['new_price'] else None,  # Giữ nguyên như CharField
                    viewed=int(row['view']),
                    sub_category=sub_category,
                    publication_year=row['publication_year'],
                    publisher=row['publisher'],
                    author=row['author'],
                    reprint_edition=row['reprint_edition'],
                    dimensions=row['dimensions'],
                    cover_type=row['cover_type'],
                    is_delete=False,  # Mặc định không bị xóa
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


