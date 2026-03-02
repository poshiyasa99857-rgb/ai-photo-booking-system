from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsViewSet, OperationLogViewSet
from .feedback_views import FeedbackViewSet, SystemConfigViewSet

router = DefaultRouter()
router.register(r'analytics', AnalyticsViewSet, basename='analytics')
router.register(r'logs', OperationLogViewSet, basename='operation-log')
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')
router.register(r'configs', SystemConfigViewSet, basename='system-config')

urlpatterns = [
    path('', include(router.urls)),
]
