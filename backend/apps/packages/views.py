from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Package, Photographer
from .serializers import (
    CategorySerializer, 
    PackageListSerializer, 
    PackageDetailSerializer,
    PhotographerSerializer
)
from apps.ai_services.deepseek_client import DeepSeekClient


class CategoryViewSet(viewsets.ModelViewSet):
    """分类视图集"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class PackageViewSet(viewsets.ModelViewSet):
    """套餐视图集"""
    queryset = Package.objects.filter(status='active')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'has_costume']
    search_fields = ['name', 'description', 'tags']
    ordering_fields = ['current_price', 'created_at', 'booking_count', 'view_count']
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PackageDetailSerializer
        return PackageListSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """查看详情时增加浏览量"""
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def generate_description(self, request, pk=None):
        """AI生成套餐描述"""
        package = self.get_object()
        
        # 调用DeepSeek生成描述
        client = DeepSeekClient()
        prompt = f"""
        请为以下摄影套餐生成一段吸引人的营销文案（100-200字）：
        套餐名称：{package.name}
        分类：{package.category.name}
        价格：{package.current_price}元
        底片数量：{package.base_photo_count}张
        精修数量：{package.retouch_count}张
        包含服装妆造：{'是' if package.has_costume else '否'}
        拍摄地点：{package.location}
        """
        
        try:
            description = client.generate_text(prompt)
            package.ai_description = description
            package.save()
            return Response({
                'message': '生成成功',
                'description': description
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    @action(detail=False, methods=['post'])
    def recommend(self, request):
        """AI智能推荐"""
        user_input = request.data.get('query', '')
        
        if not user_input:
            return Response({'error': '请输入需求描述'}, status=400)
        
        # 获取所有套餐
        packages = Package.objects.filter(status='active')
        packages_data = PackageListSerializer(packages, many=True).data
        
        # 调用DeepSeek进行推荐
        client = DeepSeekClient()
        prompt = f"""
        用户需求：{user_input}
        
        可选套餐：
        {packages_data}
        
        请分析用户需求，推荐最适合的3个套餐，并说明推荐理由。
        返回JSON格式：{{"recommendations": [{{"package_id": id, "reason": "推荐理由"}}]}}
        """
        
        try:
            result = client.generate_text(prompt)
            return Response({'recommendations': result})
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class PhotographerViewSet(viewsets.ModelViewSet):
    """摄影师视图集"""
    queryset = Photographer.objects.filter(is_verified=True)
    serializer_class = PhotographerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['style_tags']
    search_fields = ['user__username', 'bio']
    permission_classes = [AllowAny]
