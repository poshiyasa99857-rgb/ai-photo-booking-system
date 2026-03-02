from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    """预约序列化器"""
    package_name = serializers.CharField(source='package.name', read_only=True)
    package_image = serializers.ImageField(source='package.cover_image', read_only=True)
    photographer_name = serializers.CharField(source='photographer.user.username', read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'total_price', 'is_paid', 'ai_shooting_guide']


class BookingCreateSerializer(serializers.ModelSerializer):
    """创建预约序列化器"""
    
    class Meta:
        model = Booking
        fields = ['package', 'photographer', 'booking_date', 'booking_time', 
                  'photo_count', 'retouch_count', 'has_costume',
                  'contact_name', 'contact_phone', 'remark']
    
    def validate(self, attrs):
        # 计算总价
        package = attrs['package']
        base_price = package.current_price
        
        # 额外底片费用（假设每张10元）
        extra_photos = max(0, attrs['photo_count'] - package.base_photo_count)
        photo_extra_cost = extra_photos * 10
        
        # 额外精修费用（假设每张20元）
        extra_retouch = max(0, attrs['retouch_count'] - package.retouch_count)
        retouch_extra_cost = extra_retouch * 20
        
        # 服装妆造费用（假设100元）
        costume_cost = 100 if attrs['has_costume'] and not package.has_costume else 0
        
        attrs['total_price'] = base_price + photo_extra_cost + retouch_extra_cost + costume_cost
        attrs['deposit'] = attrs['total_price'] * 0.3  # 定金30%
        
        return attrs
