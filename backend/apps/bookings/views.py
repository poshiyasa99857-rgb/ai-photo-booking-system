from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer
from apps.ai_services.deepseek_client import DeepSeekClient


class BookingViewSet(viewsets.ModelViewSet):
    """预约视图集"""
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer
    
    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        
        # 生成AI拍摄建议
        self._generate_shooting_guide(booking)
        
        # 增加套餐预约量
        package = booking.package
        package.booking_count += 1
        package.save()
    
    def _generate_shooting_guide(self, booking):
        """生成AI拍摄建议"""
        client = DeepSeekClient()
        
        prompt = f"""
        请为以下摄影预约生成个性化拍摄指南：
        
        套餐类型：{booking.package.name}
        拍摄地点：{booking.package.location}
        预约日期：{booking.booking_date}
        预约时间：{booking.booking_time}
        是否包含服装妆造：{'是' if booking.has_costume else '否'}
        
        请提供：
        1. 穿搭建议
        2. 最佳拍摄时段建议
        3. 注意事项
        4. 姿势推荐
        
        用中文回答，格式清晰。
        """
        
        try:
            guide = client.generate_text(prompt)
            booking.ai_shooting_guide = guide
            booking.save()
        except Exception as e:
            print(f"生成拍摄建议失败: {e}")
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """取消预约"""
        booking = self.get_object()
        
        if booking.status == 'completed':
            return Response({'error': '已完成订单不能取消'}, status=400)
        
        booking.status = 'cancelled'
        booking.save()
        
        return Response({'message': '预约已取消'})
    
    @action(detail=True, methods=['post'])
    def reschedule(self, request, pk=None):
        """改期"""
        booking = self.get_object()
        
        if booking.status == 'completed':
            return Response({'error': '已完成订单不能改期'}, status=400)
        
        new_date = request.data.get('booking_date')
        new_time = request.data.get('booking_time')
        
        if not new_date or not new_time:
            return Response({'error': '请提供新的预约日期和时间'}, status=400)
        
        booking.booking_date = new_date
        booking.booking_time = new_time
        booking.save()
        
        return Response({
            'message': '预约已改期',
            'booking': BookingSerializer(booking).data
        })
