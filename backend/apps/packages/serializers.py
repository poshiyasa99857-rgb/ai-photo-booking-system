from rest_framework import serializers
from .models import Category, Package, Photographer


class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    
    class Meta:
        model = Category
        fields = '__all__'


class PackageListSerializer(serializers.ModelSerializer):
    """套餐列表序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Package
        fields = ['id', 'name', 'category_name', 'current_price', 'original_price', 
                  'cover_image', 'base_photo_count', 'retouch_count', 'has_costume',
                  'tags', 'view_count', 'booking_count', 'created_at']


class PackageDetailSerializer(serializers.ModelSerializer):
    """套餐详情序列化器"""
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Package
        fields = '__all__'


class PhotographerSerializer(serializers.ModelSerializer):
    """摄影师序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    
    class Meta:
        model = Photographer
        fields = ['id', 'username', 'avatar', 'bio', 'style_tags', 'experience_years', 'works', 'rating', 'is_verified']
