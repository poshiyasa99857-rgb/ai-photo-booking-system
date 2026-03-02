from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ForumCategoryViewSet, ForumPostViewSet, ForumCommentViewSet

router = DefaultRouter()
router.register(r'categories', ForumCategoryViewSet, basename='forum-category')
router.register(r'posts', ForumPostViewSet, basename='forum-post')
router.register(r'comments', ForumCommentViewSet, basename='forum-comment')

urlpatterns = [
    path('', include(router.urls)),
]
