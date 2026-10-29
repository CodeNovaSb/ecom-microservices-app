from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "product_image",
            "alt_text",
            "stock_quantity",
        ]
        read_only_fields = ["id"]