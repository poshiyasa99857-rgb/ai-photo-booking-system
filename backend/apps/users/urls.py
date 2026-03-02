from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserFavoriteViewSet, UserReviewViewSet
from .notification_views import NotificationViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'favorites', UserFavoriteViewSet, basename='favorite')
router.register(r'reviews', UserReviewViewSet, basename='review')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
