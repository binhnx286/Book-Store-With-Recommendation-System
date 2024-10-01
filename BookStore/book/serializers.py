from rest_framework import serializers
from .models import Product , Category  , SubCategory

class ProductSerializer(serializers.ModelSerializer):
    sub_category = serializers.CharField(source='sub_category.name', read_only=True)
    class Meta:
        model = Product
        fields = '__all__' 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'