from decimal import Decimal
from venv import create
from rest_framework import serializers
from .models import Collection, Review, Product

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name','description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return  Review.objects.create(product_id=product_id, **validated_data)

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price',  'collection', 'slug', 'description']
        price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

        def calculate_tax(self, product: Product):
            return product.unit_price * Decimal(1.1)