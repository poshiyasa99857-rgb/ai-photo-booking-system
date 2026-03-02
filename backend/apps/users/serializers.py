from rest_framework import serializers
from .models import User, UserFavorite, UserReview


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'avatar', 'gender', 'birthday', 'address', 'is_photographer', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'confirm_password']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('两次密码不一致')
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class UserFavoriteSerializer(serializers.ModelSerializer):
    """用户收藏序列化器"""
    package_name = serializers.CharField(source='package.name', read_only=True)
    package_image = serializers.ImageField(source='package.cover_image', read_only=True)
    
    class Meta:
        model = UserFavorite
        fields = ['id', 'package', 'package_name', 'package_image', 'created_at']


class UserReviewSerializer(serializers.ModelSerializer):
    """用户评价序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    
    class Meta:
        model = UserReview
        fields = ['id', 'user', 'username', 'avatar', 'package', 'rating', 'content', 'images', 'created_at']
        read_only_fields = ['user']
