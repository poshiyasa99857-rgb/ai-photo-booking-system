from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .deepseek_client import DeepSeekClient


class AIServiceViewSet(viewsets.ViewSet):
    """AI服务视图集"""
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def chat(self, request):
        """AI智能客服"""
        message = request.data.get('message', '')
        history = request.data.get('history', [])
        
        if not message:
            return Response({'error': '请输入消息'}, status=400)
        
        client = DeepSeekClient()
        
        # 构建消息历史
        messages = [
            {'role': 'system', 'content': '''你是摄影预约平台的智能客服助手。你可以帮助用户：
1. 了解摄影套餐详情和价格
2. 解答预约流程相关问题
3. 推荐适合的套餐
4. 回答拍摄相关咨询
请用友好、专业的语气回答用户问题。'''}
        ]
        
        # 添加历史对话
        for msg in history:
            messages.append(msg)
        
        # 添加当前消息
        messages.append({'role': 'user', 'content': message})
        
        try:
            reply = client.chat(messages)
            return Response({
                'reply': reply,
                'history': messages + [{'role': 'assistant', 'content': reply}]
            })
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    @action(detail=False, methods=['post'])
    def recommend(self, request):
        """AI智能推荐"""
        query = request.data.get('query', '')
        
        if not query:
            return Response({'error': '请输入需求描述'}, status=400)
        
        client = DeepSeekClient()
        
        prompt = f"""
        用户想要：{query}
        
        请作为摄影顾问，分析用户需求并给出推荐建议。
        包括：
        1. 需求分析
        2. 推荐的套餐类型
        3. 拍摄建议
        4. 预算参考
        """
        
        try:
            recommendation = client.generate_text(prompt)
            return Response({'recommendation': recommendation})
        except Exception as e:
            return Response({'error': str(e)}, status=500)
