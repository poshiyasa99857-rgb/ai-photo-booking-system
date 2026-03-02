from django.db import models


class Notification(models.Model):
    """站内消息通知"""
    
    TYPE_CHOICES = [
        ('system', '系统通知'),
        ('booking', '预约提醒'),
        ('payment', '支付通知'),
        ('ai_guide', 'AI拍摄建议'),
        ('forum', '论坛互动'),
    ]
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='notifications', verbose_name='用户')
    
    type = models.CharField('类型', max_length=20, choices=TYPE_CHOICES)
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    
    # 关联对象
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, 
                                related_name='notifications', verbose_name='关联预约',
                                blank=True, null=True)
    
    # 状态
    is_read = models.BooleanField('是否已读', default=False)
    read_at = models.DateTimeField('阅读时间', blank=True, null=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '站内通知'
        verbose_name_plural = verbose_name
        db_table = 'notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.title}'
