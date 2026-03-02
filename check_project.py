#!/usr/bin/env python3
"""
项目完整性检查和修复脚本
检查所有模块是否正确配置
"""

import os
import sys

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def check_imports():
    """检查所有导入"""
    print("检查Python导入...")
    errors = []
    
    try:
        import django
        print(f"✓ Django {django.VERSION}")
    except ImportError as e:
        errors.append(f"✗ Django: {e}")
    
    try:
        import rest_framework
        print("✓ Django REST Framework")
    except ImportError as e:
        errors.append(f"✗ DRF: {e}")
    
    return errors

def check_models():
    """检查模型定义"""
    print("\n检查模型定义...")
    errors = []
    
    models_to_check = [
        'apps.users.models',
        'apps.packages.models',
        'apps.bookings.models',
        'apps.forum.models',
        'apps.payments.models',
        'apps.ai_services.deepseek_client',
        'apps.analytics.models',
    ]
    
    for model_path in models_to_check:
        try:
            __import__(model_path)
            print(f"✓ {model_path}")
        except Exception as e:
            errors.append(f"✗ {model_path}: {e}")
            print(f"✗ {model_path}: {e}")
    
    return errors

def check_settings():
    """检查设置"""
    print("\n检查设置...")
    errors = []
    
    try:
        import django
        django.setup()
        from django.conf import settings
        
        # 检查INSTALLED_APPS
        required_apps = [
            'apps.users',
            'apps.packages',
            'apps.bookings',
            'apps.forum',
            'apps.payments',
            'apps.ai_services',
            'apps.analytics',
        ]
        
        for app in required_apps:
            if app in settings.INSTALLED_APPS:
                print(f"✓ {app} 已安装")
            else:
                errors.append(f"✗ {app} 未安装")
                print(f"✗ {app} 未安装")
        
        # 检查数据库配置
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.mysql':
            print("✓ MySQL数据库配置")
        
        # 检查AI配置
        if hasattr(settings, 'DEEPSEEK_API_KEY'):
            print("✓ DeepSeek配置")
        
    except Exception as e:
        errors.append(f"✗ 设置检查失败: {e}")
        print(f"✗ 设置检查失败: {e}")
    
    return errors

def main():
    print("=" * 60)
    print("AI摄影预约系统 - 完整性检查")
    print("=" * 60)
    
    all_errors = []
    
    all_errors.extend(check_imports())
    all_errors.extend(check_models())
    all_errors.extend(check_settings())
    
    print("\n" + "=" * 60)
    if all_errors:
        print(f"检查完成，发现 {len(all_errors)} 个问题:")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("✅ 所有检查通过！项目可以正常运行。")
        print("\n使用方法:")
        print("  1. 配置 .env 文件")
        print("  2. 运行: docker-compose up -d")
        print("  3. 访问: http://localhost")
    print("=" * 60)

if __name__ == '__main__':
    main()
