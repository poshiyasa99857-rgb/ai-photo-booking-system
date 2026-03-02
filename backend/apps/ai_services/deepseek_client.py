import os
import requests
from django.conf import settings


class DeepSeekClient:
    """DeepSeek AI客户端"""
    
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.api_base = settings.DEEPSEEK_API_BASE
        
    def generate_text(self, prompt, temperature=0.7, max_tokens=1000):
        """生成文本"""
        if not self.api_key:
            return "AI服务未配置，请设置DEEPSEEK_API_KEY"
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'system', 'content': '你是一个专业的摄影顾问助手，擅长为用户提供摄影相关的建议和服务。'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        
        try:
            response = requests.post(
                f'{self.api_base}/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"DeepSeek API调用失败: {e}")
            return f"AI服务暂时不可用，请稍后重试"
    
    def chat(self, messages, temperature=0.7):
        """多轮对话"""
        if not self.api_key:
            return "AI服务未配置"
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'deepseek-chat',
            'messages': messages,
            'temperature': temperature,
            'max_tokens': 2000
        }
        
        try:
            response = requests.post(
                f'{self.api_base}/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"DeepSeek API调用失败: {e}")
            return "AI服务暂时不可用"
