from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from .feedback_models import Feedback, SystemConfig
from .feedback_serializers import (
    FeedbackSerializer, 
    FeedbackCreateSerializer, 
    FeedbackReplySerializer,
    SystemConfigSerializer
)


class FeedbackViewSet(viewsets.ModelViewSet):
    """意见反馈视图集"""
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_admin:
            return Feedback.objects.all()
        return Feedback.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return FeedbackCreateSerializer
        elif self.action == 'reply':
            return FeedbackReplySerializer
        return FeedbackSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reply(self, request, pk=None):
        """管理员回复反馈"""
        feedback = self.get_object()
        serializer = self.get_serializer(feedback, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save(
                replied_by=request.user,
                replied_at=timezone.now(),
                status='resolved'
            )
            return Response(FeedbackSerializer(feedback).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        """用户对反馈处理结果评分"""
        feedback = self.get_object()
        
        # 只能评价自己的反馈
        if feedback.user != request.user:
            return Response({'error': '无权评价'}, status=403)
        
        satisfaction = request.data.get('satisfaction')
        if not satisfaction or not 1 <= int(satisfaction) <= 5:
            return Response({'error': '评分必须在1-5之间'}, status=400)
        
        feedback.satisfaction = int(satisfaction)
        feedback.save()
        
        return Response({'message': '评价成功', 'satisfaction': feedback.satisfaction})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def statistics(self, request):
        """反馈统计"""
        from django.db.models import Count, Avg
        
        total = Feedback.objects.count()
        pending = Feedback.objects.filter(status='pending').count()
        resolved = Feedback.objects.filter(status='resolved').count()
        avg_satisfaction = Feedback.objects.filter(satisfaction__isnull=False).aggregate(
            avg=Avg('satisfaction')
        )['avg']
        
        type_distribution = Feedback.objects.values('type').annotate(
            count=Count('id')
        )
        
        return Response({
            'total': total,
            'pending': pending,
            'resolved': resolved,
            'avg_satisfaction': round(avg_satisfaction, 2) if avg_satisfaction else None,
            'type_distribution': list(type_distribution),
        })


class SystemConfigViewSet(viewsets.ModelViewSet):
    """系统配置视图集"""
    queryset = SystemConfig.objects.all()
    serializer_class = SystemConfigSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def public(self, request):
        """获取公开配置"""
        configs = SystemConfig.objects.filter(is_public=True)
        return Response({c.key: c.value for c in configs})
