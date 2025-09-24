# products/serializers.py
from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(write_only=True, source="category", queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ["id", "title", "slug", "description", "price", "category", "category_id", "stock", "is_active", "created_at"]
        read_only_fields = ["id", "slug", "created_at"]
