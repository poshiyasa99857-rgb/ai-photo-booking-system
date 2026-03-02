from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AIServiceViewSet

router = DefaultRouter()
router.register(r'services', AIServiceViewSet, basename='ai-service')

urlpatterns = [
    path('', include(router.urls)),
]
