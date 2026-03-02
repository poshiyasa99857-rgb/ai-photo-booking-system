from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import ForumCategory, ForumPost, ForumComment, ForumLike
from .serializers import (
    ForumCategorySerializer,
    ForumPostListSerializer,
    ForumPostDetailSerializer,
    ForumCommentSerializer
)


class ForumCategoryViewSet(viewsets.ModelViewSet):
    """论坛分类视图集"""
    queryset = ForumCategory.objects.filter(is_active=True)
    serializer_class = ForumCategorySerializer
    permission_classes = [AllowAny]


class ForumPostViewSet(viewsets.ModelViewSet):
    """论坛帖子视图集"""
    queryset = ForumPost.objects.filter(status='active')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ForumPostListSerializer
        return ForumPostDetailSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'like']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def retrieve(self, request, *args, **kwargs):
        """查看详情时增加浏览量"""
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        # 只允许作者修改
        if self.get_object().user != self.request.user:
            raise PermissionError('无权修改')
        serializer.save()
    
    def perform_destroy(self, instance):
        # 只允许作者删除
        if instance.user != self.request.user:
            raise PermissionError('无权删除')
        instance.status = 'deleted'
        instance.save()
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """点赞/取消点赞帖子"""
        post = self.get_object()
        user = request.user
        
        like, created = ForumLike.objects.get_or_create(user=user, post=post)
        
        if created:
            post.like_count += 1
            post.save()
            return Response({'message': '点赞成功', 'liked': True})
        else:
            like.delete()
            post.like_count -= 1
            post.save()
            return Response({'message': '取消点赞', 'liked': False})
    
    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        """评论帖子"""
        post = self.get_object()
        content = request.data.get('content')
        parent_id = request.data.get('parent_id')
        
        if not content:
            return Response({'error': '评论内容不能为空'}, status=400)
        
        comment_data = {
            'post': post.id,
            'content': content,
        }
        
        if parent_id:
            comment_data['parent'] = parent_id
        
        serializer = ForumCommentSerializer(data=comment_data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            post.comment_count += 1
            post.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ForumCommentViewSet(viewsets.ModelViewSet):
    """论坛评论视图集"""
    queryset = ForumComment.objects.filter(status='active')
    serializer_class = ForumCommentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionError('无权删除')
        instance.status = 'deleted'
        instance.save()
        # 减少帖子评论数
        post = instance.post
        post.comment_count -= 1
        post.save()
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """点赞/取消点赞评论"""
        comment = self.get_object()
        user = request.user
        
        like, created = ForumLike.objects.get_or_create(user=user, comment=comment)
        
        if created:
            comment.like_count += 1
            comment.save()
            return Response({'message': '点赞成功', 'liked': True})
        else:
            like.delete()
            comment.like_count -= 1
            comment.save()
            return Response({'message': '取消点赞', 'liked': False})
