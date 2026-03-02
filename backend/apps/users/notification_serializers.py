from rest_framework import serializers
from .notification_models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """通知序列化器"""
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'type', 'type_display', 'title', 'content', 'is_read', 'created_at']
        read_only_fields = ['user', 'type', 'title', 'content']
