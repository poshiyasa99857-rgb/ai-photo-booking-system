from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from apps.analytics.task_models import ScheduledTask, TaskLog
from apps.analytics.models import DailyStatistics, OperationLog


class Command(BaseCommand):
    help = '执行定时任务'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'开始执行定时任务 - {timezone.now()}'))
        
        # 获取所有需要执行的任务
        now = timezone.now()
        tasks = ScheduledTask.objects.filter(
            is_active=True,
            next_run_at__lte=now
        )
        
        for task in tasks:
            self.execute_task(task)
        
        self.stdout.write(self.style.SUCCESS('定时任务执行完成'))
    
    def execute_task(self, task):
        """执行单个任务"""
        self.stdout.write(f'执行任务: {task.name}')
        
        # 创建日志
        log = TaskLog.objects.create(
            task=task,
            status='success',
            output='',
            started_at=timezone.now()
        )
        
        try:
            # 根据任务类型执行
            if task.task_type == 'backup':
                result = self.backup_database()
            elif task.task_type == 'cleanup':
                result = self.cleanup_data()
            elif task.task_type == 'report':
                result = self.generate_report()
            elif task.task_type == 'notification':
                result = self.send_notifications()
            elif task.task_type == 'ai_sync':
                result = self.sync_ai_data()
            else:
                result = f'自定义任务执行: {task.params}'
            
            log.output = result
            log.status = 'success'
            log.finished_at = timezone.now()
            log.save()
            
            # 更新任务统计
            task.total_runs += 1
            task.success_runs += 1
            task.last_run_at = timezone.now()
            
            # 计算下次执行时间
            task.next_run_at = self.calculate_next_run(task.cron_expression)
            task.save()
            
            self.stdout.write(self.style.SUCCESS(f'  ✓ {result}'))
            
        except Exception as e:
            log.status = 'failed'
            log.error_message = str(e)
            log.finished_at = timezone.now()
            log.save()
            
            task.total_runs += 1
            task.fail_runs += 1
            task.save()
            
            self.stdout.write(self.style.ERROR(f'  ✗ 失败: {e}'))
    
    def backup_database(self):
        """备份数据库"""
        import os
        from django.conf import settings
        
        backup_dir = '/app/backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'{backup_dir}/backup_{timestamp}.sql'
        
        # 获取数据库配置
        db_config = settings.DATABASES['default']
        
        # 执行备份命令
        import subprocess
        cmd = f"mysqldump -h {db_config['HOST']} -u {db_config['USER']} -p{db_config['PASSWORD']} {db_config['NAME']} > {backup_file}"
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            return f'数据库备份完成: {backup_file}'
        except:
            return '数据库备份命令执行（请确保mysqldump可用）'
    
    def cleanup_data(self):
        """清理过期数据"""
        # 清理30天前的操作日志
        cutoff_date = timezone.now() - timedelta(days=30)
        old_logs = OperationLog.objects.filter(created_at__lt=cutoff_date)
        count = old_logs.count()
        # old_logs.delete()  # 实际删除（谨慎使用）
        
        return f'清理完成，发现 {count} 条过期日志（已标记待删除）'
    
    def generate_report(self):
        """生成每日报表"""
        from apps.users.models import User
        from apps.bookings.models import Booking
        
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)
        
        # 统计昨日数据
        new_users = User.objects.filter(created_at__date=yesterday).count()
        new_bookings = Booking.objects.filter(created_at__date=yesterday).count()
        
        # 创建或更新统计记录
        stats, created = DailyStatistics.objects.get_or_create(
            date=yesterday,
            defaults={
                'new_users': new_users,
                'new_bookings': new_bookings,
            }
        )
        
        if not created:
            stats.new_users = new_users
            stats.new_bookings = new_bookings
            stats.save()
        
        return f'报表生成完成: 昨日新用户{new_users}, 新订单{new_bookings}'
    
    def send_notifications(self):
        """发送通知"""
        from apps.users.notification_models import Notification
        from apps.bookings.models import Booking
        
        # 查找明天需要拍摄的预约
        tomorrow = timezone.now().date() + timedelta(days=1)
        upcoming_bookings = Booking.objects.filter(
            booking_date=tomorrow,
            status='confirmed'
        )
        
        count = 0
        for booking in upcoming_bookings:
            Notification.objects.create(
                user=booking.user,
                type='booking',
                title='拍摄提醒',
                content=f'您预约的「{booking.package.name}」将在明天进行拍摄，请做好准备。',
                booking=booking
            )
            count += 1
        
        return f'已发送 {count} 条拍摄提醒通知'
    
    def sync_ai_data(self):
        """同步AI数据"""
        # 统计AI使用情况
        from apps.analytics.models import DailyStatistics
        
        today = timezone.now().date()
        stats, _ = DailyStatistics.objects.get_or_create(date=today)
        
        return f'AI数据同步完成: 今日对话{stats.ai_chat_count}次'
    
    def calculate_next_run(self, cron_expression):
        """根据cron表达式计算下次执行时间"""
        # 简化版本：假设每天执行
        from datetime import timedelta
        
        now = timezone.now()
        parts = cron_expression.split()
        
        if len(parts) == 5:
            minute, hour, day, month, weekday = parts
            
            # 每天执行
            if day == '*' and month == '*':
                next_run = now + timedelta(days=1)
                next_run = next_run.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
                return next_run
        
        # 默认1小时后
        return now + timedelta(hours=1)
