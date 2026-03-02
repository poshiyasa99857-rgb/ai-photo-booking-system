from django.db import models


class ForumCategory(models.Model):
    """论坛分类"""
    name = models.CharField('分类名称', max_length=50)
    description = models.TextField('分类描述', blank=True)
    icon = models.CharField('图标', max_length=50, blank=True)
    sort_order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '论坛分类'
        verbose_name_plural = verbose_name
        db_table = 'forum_categories'
        ordering = ['sort_order']
    
    def __str__(self):
        return self.name


class ForumPost(models.Model):
    """论坛帖子"""
    
    STATUS_CHOICES = [
        ('active', '正常'),
        ('hidden', '隐藏'),
        ('deleted', '已删除'),
    ]
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='forum_posts', verbose_name='作者')
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name='posts', verbose_name='分类')
    
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    images = models.JSONField('图片', default=list, blank=True)
    
    # 统计
    view_count = models.IntegerField('浏览量', default=0)
    like_count = models.IntegerField('点赞数', default=0)
    comment_count = models.IntegerField('评论数', default=0)
    
    # 状态
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='active')
    is_top = models.BooleanField('是否置顶', default=False)
    is_essence = models.BooleanField('是否精华', default=False)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '论坛帖子'
        verbose_name_plural = verbose_name
        db_table = 'forum_posts'
        ordering = ['-is_top', '-created_at']
    
    def __str__(self):
        return self.title


class ForumComment(models.Model):
    """论坛评论"""
    
    STATUS_CHOICES = [
        ('active', '正常'),
        ('hidden', '隐藏'),
        ('deleted', '已删除'),
    ]
    
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments', verbose_name='帖子')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='forum_comments', verbose_name='作者')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', 
                               verbose_name='父评论', blank=True, null=True)
    
    content = models.TextField('内容')
    like_count = models.IntegerField('点赞数', default=0)
    
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '论坛评论'
        verbose_name_plural = verbose_name
        db_table = 'forum_comments'
        ordering = ['created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.content[:50]}'


class ForumLike(models.Model):
    """论坛点赞"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='likes', 
                            verbose_name='帖子', blank=True, null=True)
    comment = models.ForeignKey(ForumComment, on_delete=models.CASCADE, related_name='likes',
                               verbose_name='评论', blank=True, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '论坛点赞'
        verbose_name_plural = verbose_name
        db_table = 'forum_likes'
        unique_together = [
            ['user', 'post'],
            ['user', 'comment'],
        ]
