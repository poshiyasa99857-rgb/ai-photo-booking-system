from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserFavoriteViewSet, UserReviewViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'favorites', UserFavoriteViewSet, basename='favorite')
router.register(r'reviews', UserReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
