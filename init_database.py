#!/usr/bin/env python
"""
数据库初始化脚本
创建数据库表并导入初始数据
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
django.setup()

from django.db import connection
from apps.users.models import User
from apps.packages.models import Category, Package
from apps.forum.models import ForumCategory


def init_database():
    """初始化数据库"""
    print("开始初始化数据库...")
    
    # 创建超级管理员
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            phone='13800138000'
        )
        print("✓ 创建超级管理员: admin / admin123")
    
    # 创建套餐分类
    categories_data = [
        {'name': '婚纱摄影', 'description': '记录爱情最美好的时刻', 'icon': 'heart'},
        {'name': '个人写真', 'description': '展现最美的自己', 'icon': 'user'},
        {'name': '亲子摄影', 'description': '定格温馨亲子时光', 'icon': 'smile'},
        {'name': '商业拍摄', 'description': '专业商业摄影服务', 'icon': 'camera'},
        {'name': '旅拍', 'description': '边走边拍，记录旅途美好', 'icon': 'global'},
    ]
    
    for cat_data in categories_data:
        Category.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
    print(f"✓ 创建套餐分类: {len(categories_data)}个")
    
    # 创建示例套餐
    if Package.objects.count() == 0:
        category = Category.objects.first()
        Package.objects.create(
            name='经典婚纱摄影套餐',
            category=category,
            description='包含室内外多场景拍摄，专业化妆师全程跟妆，精修50张照片',
            original_price=5999,
            current_price=3999,
            base_photo_count=200,
            retouch_count=50,
            final_photo_count=50,
            has_costume=True,
            duration=8,
            location='市内多个景点',
            tags=['婚纱', '经典', '热门'],
            status='active'
        )
        print("✓ 创建示例套餐")
    
    # 创建论坛分类
    forum_categories = [
        {'name': '拍摄经验', 'description': '分享拍摄技巧和心得'},
        {'name': '作品展示', 'description': '展示您的摄影作品'},
        {'name': '器材讨论', 'description': '摄影器材交流'},
        {'name': '约拍信息', 'description': '寻找摄影伙伴'},
        {'name': '问题求助', 'description': '遇到问题来这里问'},
    ]
    
    for cat_data in forum_categories:
        ForumCategory.objects.get_or_create(name=cat_data['name'], defaults=cat_data)
    print(f"✓ 创建论坛分类: {len(forum_categories)}个")
    
    print("\n数据库初始化完成！")
    print("\n管理员账号:")
    print("  用户名: admin")
    print("  密码: admin123")


if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        print(f"初始化失败: {e}")
        sys.exit(1)
