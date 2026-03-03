from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsViewSet, OperationLogViewSet
from .feedback_views import FeedbackViewSet, SystemConfigViewSet
from .task_views import ScheduledTaskViewSet, TaskLogViewSet

router = DefaultRouter()
router.register(r'analytics', AnalyticsViewSet, basename='analytics')
router.register(r'logs', OperationLogViewSet, basename='operation-log')
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')
router.register(r'configs', SystemConfigViewSet, basename='system-config')
router.register(r'tasks', ScheduledTaskViewSet, basename='scheduled-task')
router.register(r'task-logs', TaskLogViewSet, basename='task-log')

urlpatterns = [
    path('', include(router.urls)),
]
