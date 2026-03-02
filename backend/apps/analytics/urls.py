from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsViewSet, OperationLogViewSet

router = DefaultRouter()
router.register(r'analytics', AnalyticsViewSet, basename='analytics')
router.register(r'logs', OperationLogViewSet, basename='operation-log')

urlpatterns = [
    path('', include(router.urls)),
]
