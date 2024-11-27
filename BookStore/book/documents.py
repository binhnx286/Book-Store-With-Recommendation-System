from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Product

@registry.register_document
class ProductDocument(Document):
    sub_category = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.TextField(),
    })

    # Thêm trường description
    description = fields.TextField(attr="clean_description")

    class Index:
        name = 'products'  # Tên chỉ mục Elasticsearch

    class Django:
        model = Product  # Model Django
        fields = [
            'id',
            'name',
            'quantity',
            'price_origin',
            'new_price',
            'viewed',
            'publication_year',
            'publisher',
            'author',
            'reprint_edition',
            'dimensions',
            'cover_type',
            'is_delete',
        ]

    # Trường tìm kiếm liên quan
    related_models = ['SubCategory']
