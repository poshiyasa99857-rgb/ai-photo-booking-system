from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ScheduledTask(models.Model):
    """定时任务"""
    
    TASK_TYPE_CHOICES = [
        ('backup', '数据备份'),
        ('cleanup', '数据清理'),
        ('report', '生成报表'),
        ('notification', '发送通知'),
        ('ai_sync', 'AI数据同步'),
        ('custom', '自定义任务'),
    ]
    
    STATUS_CHOICES = [
        ('pending', '待执行'),
        ('running', '执行中'),
        ('success', '成功'),
        ('failed', '失败'),
    ]
    
    name = models.CharField('任务名称', max_length=100)
    task_type = models.CharField('任务类型', max_length=20, choices=TASK_TYPE_CHOICES)
    
    # 定时规则（cron表达式）
    cron_expression = models.CharField('Cron表达式', max_length=100, 
                                       help_text='如: 0 0 * * * 表示每天0点')
    
    # 任务参数
    params = models.JSONField('任务参数', default=dict, blank=True)
    
    # 状态
    is_active = models.BooleanField('是否启用', default=True)
    last_run_at = models.DateTimeField('上次执行时间', blank=True, null=True)
    next_run_at = models.DateTimeField('下次执行时间', blank=True, null=True)
    
    # 执行统计
    total_runs = models.IntegerField('总执行次数', default=0)
    success_runs = models.IntegerField('成功次数', default=0)
    fail_runs = models.IntegerField('失败次数', default=0)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '定时任务'
        verbose_name_plural = verbose_name
        db_table = 'scheduled_tasks'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class TaskLog(models.Model):
    """任务执行日志"""
    
    STATUS_CHOICES = [
        ('success', '成功'),
        ('failed', '失败'),
    ]
    
    task = models.ForeignKey(ScheduledTask, on_delete=models.CASCADE, 
                            related_name='logs', verbose_name='任务')
    
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES)
    output = models.TextField('输出内容', blank=True)
    error_message = models.TextField('错误信息', blank=True)
    
    started_at = models.DateTimeField('开始时间')
    finished_at = models.DateTimeField('结束时间', blank=True, null=True)
    
    class Meta:
        verbose_name = '任务日志'
        verbose_name_plural = verbose_name
        db_table = 'task_logs'
        ordering = ['-started_at']
    
    def __str__(self):
        return f'{self.task.name} - {self.get_status_display()}'
    
    @property
    def duration(self):
        """执行时长（秒）"""
        if self.finished_at and self.started_at:
            return (self.finished_at - self.started_at).total_seconds()
        return None
