# filters.py
from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    publication_year = filters.CharFilter(method='filter_multiple_values', field_name="publication_year")
    publisher = filters.CharFilter(method='filter_multiple_values', field_name="publisher")
    sub_category = filters.CharFilter(method='filter_multiple_values', field_name="sub_category__name")
    new_price_min = filters.NumberFilter(field_name="new_price", lookup_expr="gte")
    new_price_max = filters.NumberFilter(field_name="new_price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ['publication_year', 'publisher', 'sub_category', 'new_price_min', 'new_price_max']

    def filter_multiple_values(self, queryset, name, value):
        values = value.split(",")  # Tách các giá trị bằng dấu phẩy
       
        return queryset.filter(**{f"{name}__in": values})
