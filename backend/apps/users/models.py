from django.contrib.auth.models import AbstractUser
from django.db import models
from .notification_models import Notification


class User(AbstractUser):
    """自定义用户模型"""
    
    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
        ('other', '其他'),
    ]
    
    phone = models.CharField('手机号', max_length=11, unique=True, blank=True, null=True)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    gender = models.CharField('性别', max_length=10, choices=GENDER_CHOICES, blank=True)
    birthday = models.DateField('生日', blank=True, null=True)
    address = models.CharField('地址', max_length=200, blank=True)
    is_photographer = models.BooleanField('是否摄影师', default=False)
    is_admin = models.BooleanField('是否管理员', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        db_table = 'users'
    
    def __str__(self):
        return self.username


class UserFavorite(models.Model):
    """用户收藏"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='用户')
    package = models.ForeignKey('packages.Package', on_delete=models.CASCADE, verbose_name='套餐')
    created_at = models.DateTimeField('收藏时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        db_table = 'user_favorites'
        unique_together = ['user', 'package']


class UserReview(models.Model):
    """用户评价"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='用户')
    package = models.ForeignKey('packages.Package', on_delete=models.CASCADE, verbose_name='套餐')
    rating = models.IntegerField('评分', choices=[(i, i) for i in range(1, 6)])
    content = models.TextField('评价内容')
    images = models.JSONField('评价图片', default=list, blank=True)
    is_deleted = models.BooleanField('是否删除', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '用户评价'
        verbose_name_plural = verbose_name
        db_table = 'user_reviews'
