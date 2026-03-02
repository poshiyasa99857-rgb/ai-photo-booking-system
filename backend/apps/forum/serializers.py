from rest_framework import serializers
from .models import ForumCategory, ForumPost, ForumComment, ForumLike


class ForumCategorySerializer(serializers.ModelSerializer):
    """论坛分类序列化器"""
    post_count = serializers.IntegerField(source='posts.count', read_only=True)
    
    class Meta:
        model = ForumCategory
        fields = '__all__'


class ForumCommentSerializer(serializers.ModelSerializer):
    """论坛评论序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    replies = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = ForumComment
        fields = ['id', 'user', 'username', 'avatar', 'content', 'like_count', 
                  'replies', 'is_liked', 'created_at']
        read_only_fields = ['user']
    
    def get_replies(self, obj):
        if hasattr(obj, 'replies'):
            replies = obj.replies.filter(status='active')
            return ForumCommentSerializer(replies, many=True).data
        return []
    
    def get_is_liked(self, obj):
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            return ForumLike.objects.filter(user=user, comment=obj).exists()
        return False


class ForumPostListSerializer(serializers.ModelSerializer):
    """论坛帖子列表序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = ForumPost
        fields = ['id', 'title', 'username', 'avatar', 'category_name', 
                  'view_count', 'like_count', 'comment_count', 
                  'is_top', 'is_essence', 'created_at']


class ForumPostDetailSerializer(serializers.ModelSerializer):
    """论坛帖子详情序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    category = ForumCategorySerializer(read_only=True)
    comments = ForumCommentSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()
    
    class Meta:
        model = ForumPost
        fields = '__all__'
        read_only_fields = ['user', 'view_count', 'like_count', 'comment_count']
    
    def get_is_liked(self, obj):
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            return ForumLike.objects.filter(user=user, post=obj).exists()
        return False
    
    def get_is_author(self, obj):
        user = self.context.get('request').user if self.context.get('request') else None
        return user == obj.user if user else False
