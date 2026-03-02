from rest_framework import serializers
from .models import PaymentOrder


class PaymentOrderSerializer(serializers.ModelSerializer):
    """支付订单序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    package_name = serializers.CharField(source='booking.package.name', read_only=True)
    
    class Meta:
        model = PaymentOrder
        fields = ['id', 'order_no', 'username', 'package_name', 'order_type', 
                  'amount', 'payment_method', 'status', 'pay_time', 'created_at']
        read_only_fields = ['order_no', 'user', 'status', 'pay_time']


class PaymentCreateSerializer(serializers.ModelSerializer):
    """创建支付订单序列化器"""
    
    class Meta:
        model = PaymentOrder
        fields = ['booking', 'order_type', 'payment_method']
    
    def validate(self, attrs):
        booking = attrs['booking']
        user = self.context['request'].user
        
        # 检查是否是本人预约
        if booking.user != user:
            raise serializers.ValidationError('无权为此预约创建支付')
        
        # 检查是否已支付
        if booking.is_paid:
            raise serializers.ValidationError('该预约已支付')
        
        # 计算金额
        if attrs['order_type'] == 'deposit':
            attrs['amount'] = booking.deposit
        else:
            attrs['amount'] = booking.total_price
        
        return attrs


class AlipayCallbackSerializer(serializers.Serializer):
    """支付宝回调序列化器"""
    out_trade_no = serializers.CharField()
    trade_no = serializers.CharField()
    trade_status = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
