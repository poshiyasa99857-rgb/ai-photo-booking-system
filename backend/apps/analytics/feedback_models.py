from django.db import models


class Feedback(models.Model):
    """用户意见反馈"""
    
    TYPE_CHOICES = [
        ('complaint', '投诉'),
        ('suggestion', '建议'),
        ('consultation', '咨询'),
        ('other', '其他'),
    ]
    
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('resolved', '已解决'),
        ('closed', '已关闭'),
    ]
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='feedbacks', verbose_name='用户')
    
    # 反馈内容
    type = models.CharField('反馈类型', max_length=20, choices=TYPE_CHOICES, default='suggestion')
    title = models.CharField('标题', max_length=200)
    content = models.TextField('详细内容')
    images = models.JSONField('图片', default=list, blank=True)
    contact_info = models.CharField('联系方式', max_length=100, blank=True)
    
    # 处理状态
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # 管理员回复
    reply = models.TextField('回复内容', blank=True)
    replied_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, 
                                   related_name='feedback_replies', verbose_name='回复人', 
                                   blank=True, null=True)
    replied_at = models.DateTimeField('回复时间', blank=True, null=True)
    
    # 评分（解决后用户评分）
    satisfaction = models.IntegerField('满意度', choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '意见反馈'
        verbose_name_plural = verbose_name
        db_table = 'feedbacks'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.title}'


class SystemConfig(models.Model):
    """系统配置"""
    
    key = models.CharField('配置键', max_length=100, unique=True)
    value = models.TextField('配置值')
    description = models.TextField('描述', blank=True)
    is_public = models.BooleanField('是否公开', default=False)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '系统配置'
        verbose_name_plural = verbose_name
        db_table = 'system_configs'
    
    def __str__(self):
        return self.key
    
    @classmethod
    def get_value(cls, key, default=None):
        """获取配置值"""
        try:
            config = cls.objects.get(key=key)
            return config.value
        except cls.DoesNotExist:
            return default
    
    @classmethod
    def set_value(cls, key, value, description=''):
        """设置配置值"""
        config, created = cls.objects.update_or_create(
            key=key,
            defaults={'value': value, 'description': description}
        )
        return config
