from django.db import models


class Category(models.Model):
    """套餐分类"""
    name = models.CharField('分类名称', max_length=50)
    description = models.TextField('分类描述', blank=True)
    icon = models.CharField('图标', max_length=50, blank=True)
    sort_order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '套餐分类'
        verbose_name_plural = verbose_name
        db_table = 'categories'
        ordering = ['sort_order']
    
    def __str__(self):
        return self.name


class Package(models.Model):
    """摄影套餐"""
    
    STATUS_CHOICES = [
        ('active', '上架'),
        ('inactive', '下架'),
    ]
    
    name = models.CharField('套餐名称', max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='packages', verbose_name='分类')
    description = models.TextField('套餐描述')
    ai_description = models.TextField('AI生成描述', blank=True, help_text='AI自动生成的营销文案')
    
    # 价格
    original_price = models.DecimalField('原价', max_digits=10, decimal_places=2)
    current_price = models.DecimalField('现价', max_digits=10, decimal_places=2)
    
    # 拍摄参数
    base_photo_count = models.IntegerField('底片数量', default=0, help_text='0-100张可选')
    retouch_count = models.IntegerField('精修数量', default=0, help_text='0-10张可选')
    final_photo_count = models.IntegerField('最终交付照片数', default=0)
    has_costume = models.BooleanField('包含服装妆造', default=False)
    
    # 图片
    cover_image = models.ImageField('封面图', upload_to='packages/covers/')
    sample_images = models.JSONField('样片', default=list, help_text='样片图片URL列表')
    
    # 其他
    duration = models.IntegerField('拍摄时长(小时)', default=2)
    location = models.CharField('拍摄地点', max_length=200)
    tags = models.JSONField('标签', default=list)
    
    # 状态
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='active')
    view_count = models.IntegerField('浏览量', default=0)
    booking_count = models.IntegerField('预约量', default=0)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '摄影套餐'
        verbose_name_plural = verbose_name
        db_table = 'packages'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Photographer(models.Model):
    """摄影师"""
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='photographer_profile', verbose_name='用户')
    bio = models.TextField('个人简介')
    style_tags = models.JSONField('风格标签', default=list, help_text='如["复古风", "清新风"]')
    experience_years = models.IntegerField('从业年限', default=0)
    works = models.JSONField('作品', default=list, help_text='作品图片URL列表')
    is_verified = models.BooleanField('是否认证', default=False)
    rating = models.DecimalField('评分', max_digits=2, decimal_places=1, default=5.0)
    
    class Meta:
        verbose_name = '摄影师'
        verbose_name_plural = verbose_name
        db_table = 'photographers'
    
    def __str__(self):
        return self.user.username
