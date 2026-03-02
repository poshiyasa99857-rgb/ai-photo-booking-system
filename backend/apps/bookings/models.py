from django.db import models


class Booking(models.Model):
    """预约订单"""
    
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='bookings', verbose_name='用户')
    package = models.ForeignKey('packages.Package', on_delete=models.CASCADE, related_name='bookings', verbose_name='套餐')
    photographer = models.ForeignKey('packages.Photographer', on_delete=models.SET_NULL, 
                                     related_name='bookings', verbose_name='摄影师', blank=True, null=True)
    
    # 预约时间
    booking_date = models.DateField('预约日期')
    booking_time = models.TimeField('预约时间')
    
    # 拍摄参数选择
    photo_count = models.IntegerField('底片数量', default=0)
    retouch_count = models.IntegerField('精修数量', default=0)
    has_costume = models.BooleanField('需要服装妆造', default=False)
    
    # 联系信息
    contact_name = models.CharField('联系人姓名', max_length=50)
    contact_phone = models.CharField('联系人电话', max_length=20)
    remark = models.TextField('备注', blank=True)
    
    # 价格和支付
    total_price = models.DecimalField('总价', max_digits=10, decimal_places=2)
    deposit = models.DecimalField('定金', max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField('是否支付定金', default=False)
    
    # 状态
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # AI拍摄建议
    ai_shooting_guide = models.TextField('AI拍摄建议', blank=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '预约订单'
        verbose_name_plural = verbose_name
        db_table = 'bookings'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.package.name}'
