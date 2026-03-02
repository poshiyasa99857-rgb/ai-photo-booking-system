from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class OperationLog(models.Model):
    """操作日志"""
    
    ACTION_CHOICES = [
        ('login', '登录'),
        ('logout', '退出'),
        ('create', '创建'),
        ('update', '修改'),
        ('delete', '删除'),
        ('pay', '支付'),
        ('refund', '退款'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operation_logs', verbose_name='用户')
    action = models.CharField('操作类型', max_length=20, choices=ACTION_CHOICES)
    target = models.CharField('操作对象', max_length=100)
    detail = models.TextField('详细内容', blank=True)
    ip_address = models.GenericIPAddressField('IP地址', blank=True, null=True)
    user_agent = models.TextField('User Agent', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        db_table = 'operation_logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.get_action_display()}'


class DailyStatistics(models.Model):
    """每日统计"""
    date = models.DateField('日期', unique=True)
    
    # 用户统计
    new_users = models.IntegerField('新增用户', default=0)
    active_users = models.IntegerField('活跃用户', default=0)
    total_users = models.IntegerField('总用户数', default=0)
    
    # 订单统计
    new_bookings = models.IntegerField('新预约', default=0)
    completed_bookings = models.IntegerField('完成预约', default=0)
    cancelled_bookings = models.IntegerField('取消预约', default=0)
    total_revenue = models.DecimalField('总收入', max_digits=12, decimal_places=2, default=0)
    
    # 论坛统计
    new_posts = models.IntegerField('新帖子', default=0)
    new_comments = models.IntegerField('新评论', default=0)
    
    # AI统计
    ai_chat_count = models.IntegerField('AI对话次数', default=0)
    ai_recommend_count = models.IntegerField('AI推荐次数', default=0)
    ai_token_usage = models.IntegerField('AI Token消耗', default=0)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '每日统计'
        verbose_name_plural = verbose_name
        db_table = 'daily_statistics'
        ordering = ['-date']
    
    def __str__(self):
        return str(self.date)
