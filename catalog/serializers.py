from rest_framework import serializers

from catalog.models import Category, Product


class ProductListSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        # fields = '__all__'
        # Or explicitly list fields:
        fields = ["name", "price", "photo", "category"]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model=Category
        fields=['id','name','image','slug']

class CategoryDetailSerializer(serializers.ModelSerializer):
    products=ProductListSerializer(many=True,read_only=True)
    class Meta:
        model=Category
        fields=['id','name','image','slug','products']




class ProductDetailSerializer(serializers.ModelSerializer):

    category = CategorySerializer()

    class Meta:
        model = Product
        # fields = '__all__'
        # Or explicitly list fields:
        fields = ["name", "price", "photo", "category"]
