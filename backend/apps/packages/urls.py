from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PackageViewSet, PhotographerViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'packages', PackageViewSet, basename='package')
router.register(r'photographers', PhotographerViewSet, basename='photographer')

urlpatterns = [
    path('', include(router.urls)),
]
