from rest_framework import serializers
from .task_models import ScheduledTask, TaskLog


class ScheduledTaskSerializer(serializers.ModelSerializer):
    """定时任务序列化器"""
    task_type_display = serializers.CharField(source='get_task_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ScheduledTask
        fields = '__all__'


class TaskLogSerializer(serializers.ModelSerializer):
    """任务日志序列化器"""
    task_name = serializers.CharField(source='task.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    duration = serializers.ReadOnlyField()
    
    class Meta:
        model = TaskLog
        fields = '__all__'
        read_only_fields = ['task', 'status', 'output', 'error_message', 'started_at', 'finished_at']
