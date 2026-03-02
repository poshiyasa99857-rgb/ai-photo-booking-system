from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import PaymentOrder
from .serializers import PaymentOrderSerializer, PaymentCreateSerializer
import uuid


class PaymentViewSet(viewsets.ModelViewSet):
    """支付视图集"""
    serializer_class = PaymentOrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PaymentOrder.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentOrderSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        """获取支付链接（支付宝沙盒）"""
        order = self.get_object()
        
        if order.status != 'pending':
            return Response({'error': '订单状态不正确'}, status=400)
        
        # 这里集成支付宝沙盒SDK
        # 简化版本，返回模拟数据
        pay_url = f"https://openapi.alipaydev.com/gateway.do?order_no={order.order_no}"
        
        return Response({
            'order_no': order.order_no,
            'amount': str(order.amount),
            'pay_url': pay_url,
            'message': '请使用支付宝沙盒APP扫码支付'
        })
    
    @action(detail=False, methods=['post'])
    def callback(self, request):
        """支付回调"""
        # 实际项目中需要验证支付宝签名
        order_no = request.data.get('out_trade_no')
        trade_no = request.data.get('trade_no')
        trade_status = request.data.get('trade_status')
        
        try:
            order = PaymentOrder.objects.get(order_no=order_no)
        except PaymentOrder.DoesNotExist:
            return Response({'error': '订单不存在'}, status=404)
        
        if trade_status in ['TRADE_SUCCESS', 'TRADE_FINISHED']:
            order.status = 'paid'
            order.trade_no = trade_no
            order.pay_time = timezone.now()
            order.save()
            
            # 更新预约状态
            booking = order.booking
            booking.is_paid = True
            booking.save()
            
            return Response({'message': '支付成功'})
        
        return Response({'message': '支付状态：' + trade_status})
    
    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """申请退款"""
        order = self.get_object()
        
        if order.status != 'paid':
            return Response({'error': '订单未支付'}, status=400)
        
        reason = request.data.get('reason', '')
        
        # 实际项目中调用支付宝退款接口
        order.status = 'refunded'
        order.refund_reason = reason
        order.refund_time = timezone.now()
        order.save()
        
        return Response({'message': '退款申请已提交'})


from django.utils import timezone
