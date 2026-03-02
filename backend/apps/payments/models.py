from django.db import models
import uuid


class PaymentOrder(models.Model):
    """支付订单"""
    
    STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('failed', '支付失败'),
        ('cancelled', '已取消'),
        ('refunded', '已退款'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('alipay', '支付宝'),
        ('wechat', '微信支付'),
    ]
    
    ORDER_TYPE_CHOICES = [
        ('deposit', '定金'),
        ('full', '全款'),
    ]
    
    # 订单信息
    order_no = models.CharField('订单号', max_length=64, unique=True, default=lambda: str(uuid.uuid4()).replace('-', '')[:20])
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='payments', verbose_name='用户')
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='payments', verbose_name='预约')
    
    # 支付信息
    order_type = models.CharField('订单类型', max_length=20, choices=ORDER_TYPE_CHOICES, default='deposit')
    amount = models.DecimalField('支付金额', max_digits=10, decimal_places=2)
    payment_method = models.CharField('支付方式', max_length=20, choices=PAYMENT_METHOD_CHOICES, default='alipay')
    
    # 状态
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # 第三方支付信息
    trade_no = models.CharField('第三方支付订单号', max_length=128, blank=True)
    pay_time = models.DateTimeField('支付时间', blank=True, null=True)
    
    # 退款信息
    refund_amount = models.DecimalField('退款金额', max_digits=10, decimal_places=2, default=0)
    refund_reason = models.TextField('退款原因', blank=True)
    refund_time = models.DateTimeField('退款时间', blank=True, null=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '支付订单'
        verbose_name_plural = verbose_name
        db_table = 'payment_orders'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.order_no
