from rest_framework import serializers
from .feedback_models import Feedback, SystemConfig


class FeedbackSerializer(serializers.ModelSerializer):
    """意见反馈序列化器"""
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'username', 'avatar', 'type', 'type_display', 
                  'title', 'content', 'images', 'contact_info', 'status', 'status_display',
                  'reply', 'replied_by', 'replied_at', 'satisfaction', 'created_at']
        read_only_fields = ['user', 'status', 'reply', 'replied_by', 'replied_at', 'satisfaction']


class FeedbackCreateSerializer(serializers.ModelSerializer):
    """创建反馈序列化器"""
    
    class Meta:
        model = Feedback
        fields = ['type', 'title', 'content', 'images', 'contact_info']


class FeedbackReplySerializer(serializers.ModelSerializer):
    """回复反馈序列化器"""
    
    class Meta:
        model = Feedback
        fields = ['reply', 'status']


class SystemConfigSerializer(serializers.ModelSerializer):
    """系统配置序列化器"""
    
    class Meta:
        model = SystemConfig
        fields = '__all__'
