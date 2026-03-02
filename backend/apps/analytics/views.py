from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta
from .models import DailyStatistics, OperationLog


class AnalyticsViewSet(viewsets.ViewSet):
    """统计分析视图集"""
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """管理后台首页数据"""
        from apps.users.models import User
        from apps.bookings.models import Booking
        from apps.packages.models import Package
        from apps.forum.models import ForumPost
        
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        # 用户统计
        total_users = User.objects.count()
        today_new_users = User.objects.filter(created_at__date=today).count()
        yesterday_new_users = User.objects.filter(created_at__date=yesterday).count()
        
        # 订单统计
        total_bookings = Booking.objects.count()
        today_bookings = Booking.objects.filter(created_at__date=today).count()
        pending_bookings = Booking.objects.filter(status='pending').count()
        
        # 收入统计
        total_revenue = Booking.objects.filter(is_paid=True).aggregate(
            total=Sum('total_price')
        )['total'] or 0
        
        # 套餐统计
        total_packages = Package.objects.count()
        hot_package = Package.objects.order_by('-booking_count').first()
        
        # 论坛统计
        total_posts = ForumPost.objects.count()
        today_posts = ForumPost.objects.filter(created_at__date=today).count()
        
        return Response({
            'users': {
                'total': total_users,
                'today_new': today_new_users,
                'growth': today_new_users - yesterday_new_users,
            },
            'bookings': {
                'total': total_bookings,
                'today': today_bookings,
                'pending': pending_bookings,
            },
            'revenue': {
                'total': float(total_revenue),
            },
            'packages': {
                'total': total_packages,
                'hot': hot_package.name if hot_package else None,
            },
            'forum': {
                'total_posts': total_posts,
                'today_posts': today_posts,
            },
        })
    
    @action(detail=False, methods=['get'])
    def revenue(self, request):
        """收入统计"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = DailyStatistics.objects.all()
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        data = queryset.values('date').annotate(
            revenue=Sum('total_revenue'),
            bookings=Sum('new_bookings')
        ).order_by('date')
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def ai_usage(self, request):
        """AI使用统计"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = DailyStatistics.objects.all()
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        total_chat = queryset.aggregate(total=Sum('ai_chat_count'))['total'] or 0
        total_recommend = queryset.aggregate(total=Sum('ai_recommend_count'))['total'] or 0
        total_tokens = queryset.aggregate(total=Sum('ai_token_usage'))['total'] or 0
        
        daily_data = queryset.values('date').annotate(
            chat_count=Sum('ai_chat_count'),
            recommend_count=Sum('ai_recommend_count'),
            token_usage=Sum('ai_token_usage')
        ).order_by('date')
        
        return Response({
            'total': {
                'chat': total_chat,
                'recommend': total_recommend,
                'tokens': total_tokens,
            },
            'daily': list(daily_data),
        })


class OperationLogViewSet(viewsets.ModelViewSet):
    """操作日志视图集"""
    queryset = OperationLog.objects.all()
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        queryset = OperationLog.objects.all()
        
        # 筛选
        user_id = self.request.query_params.get('user_id')
        action = self.request.query_params.get('action')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if action:
            queryset = queryset.filter(action=action)
        
        return queryset
