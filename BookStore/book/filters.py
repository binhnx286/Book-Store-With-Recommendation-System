# filters.py
from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    publication_year = filters.CharFilter(method='filter_publication_year')
    publisher = filters.CharFilter(field_name="publisher", lookup_expr="icontains")
    sub_category = filters.CharFilter(field_name="sub_category__name", lookup_expr="exact")
    new_price_min = filters.NumberFilter(field_name="new_price", lookup_expr="gte")
    new_price_max = filters.NumberFilter(field_name="new_price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ['publication_year', 'publisher', 'sub_category', 'new_price_min', 'new_price_max']

    def filter_publication_year(self, queryset, name, value):
        years = value.split(",")  # Tách các năm bằng dấu phẩy
        return queryset.filter(publication_year__in=years)
