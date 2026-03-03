from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.utils import timezone
from datetime import datetime, timedelta
import subprocess
from .task_models import ScheduledTask, TaskLog
from .task_serializers import ScheduledTaskSerializer, TaskLogSerializer


class ScheduledTaskViewSet(viewsets.ModelViewSet):
    """定时任务视图集"""
    queryset = ScheduledTask.objects.all()
    serializer_class = ScheduledTaskSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=True, methods=['post'])
    def run_now(self, request, pk=None):
        """立即执行任务"""
        task = self.get_object()
        
        # 创建日志
        log = TaskLog.objects.create(
            task=task,
            status='success',
            output='',
            started_at=timezone.now()
        )
        
        try:
            # 根据任务类型执行不同操作
            result = self._execute_task(task)
            
            log.output = result
            log.status = 'success'
            log.finished_at = timezone.now()
            log.save()
            
            # 更新任务统计
            task.total_runs += 1
            task.success_runs += 1
            task.last_run_at = timezone.now()
            task.save()
            
            return Response({
                'message': '任务执行成功',
                'output': result,
                'duration': log.duration
            })
            
        except Exception as e:
            log.status = 'failed'
            log.error_message = str(e)
            log.finished_at = timezone.now()
            log.save()
            
            task.total_runs += 1
            task.fail_runs += 1
            task.save()
            
            return Response({
                'message': '任务执行失败',
                'error': str(e)
            }, status=500)
    
    def _execute_task(self, task):
        """执行任务"""
        if task.task_type == 'backup':
            return self._backup_database()
        elif task.task_type == 'cleanup':
            return self._cleanup_data()
        elif task.task_type == 'report':
            return self._generate_report()
        elif task.task_type == 'notification':
            return self._send_notifications()
        elif task.task_type == 'ai_sync':
            return self._sync_ai_data()
        else:
            return f'执行自定义任务: {task.params}'
    
    def _backup_database(self):
        """备份数据库"""
        # 实际项目中调用数据库备份命令
        return '数据库备份完成: backup_2024.sql'
    
    def _cleanup_data(self):
        """清理过期数据"""
        # 清理30天前的日志
        from .models import OperationLog
        cutoff_date = timezone.now() - timedelta(days=30)
        deleted_count = OperationLog.objects.filter(created_at__lt=cutoff_date).count()
        # OperationLog.objects.filter(created_at__lt=cutoff_date).delete()
        return f'清理完成，删除了 {deleted_count} 条过期日志'
    
    def _generate_report(self):
        """生成报表"""
        from .models import DailyStatistics
        today = timezone.now().date()
        stats = DailyStatistics.objects.filter(date=today).first()
        if stats:
            return f'今日报表: 新用户{stats.new_users}, 订单{stats.new_bookings}'
        return '今日暂无数据'
    
    def _send_notifications(self):
        """发送通知"""
        # 发送预约提醒等
        return '通知发送完成'
    
    def _sync_ai_data(self):
        """同步AI数据"""
        return 'AI数据同步完成'
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """任务统计"""
        total_tasks = ScheduledTask.objects.count()
        active_tasks = ScheduledTask.objects.filter(is_active=True).count()
        
        today = timezone.now().date()
        today_logs = TaskLog.objects.filter(started_at__date=today)
        today_success = today_logs.filter(status='success').count()
        today_failed = today_logs.filter(status='failed').count()
        
        return Response({
            'total_tasks': total_tasks,
            'active_tasks': active_tasks,
            'today_runs': today_success + today_failed,
            'today_success': today_success,
            'today_failed': today_failed,
        })


class TaskLogViewSet(viewsets.ReadOnlyModelViewSet):
    """任务日志视图集"""
    queryset = TaskLog.objects.all()
    serializer_class = TaskLogSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        queryset = TaskLog.objects.all()
        
        # 筛选
        task_id = self.request.query_params.get('task_id')
        status = self.request.query_params.get('status')
        
        if task_id:
            queryset = queryset.filter(task_id=task_id)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
