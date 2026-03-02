#!/bin/bash
# 配置脚本 - 帮助设置 AI 和支付

echo "================================"
echo "AI摄影预约系统 - 配置向导"
echo "================================"
echo ""

# 检查 .env 文件是否存在
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ 已创建 .env 文件"
fi

echo "请选择要配置的功能："
echo ""
echo "1) 配置 DeepSeek AI"
echo "2) 配置支付宝沙盒"
echo "3) 配置两者"
echo "4) 跳过配置"
echo ""
read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "--- DeepSeek AI 配置 ---"
        echo "1. 访问 https://platform.deepseek.com"
        echo "2. 注册并创建 API Key"
        echo ""
        read -p "请输入 DeepSeek API Key: " deepseek_key
        
        # 更新 .env
        if grep -q "DEEPSEEK_API_KEY=" .env; then
            sed -i "s/DEEPSEEK_API_KEY=.*/DEEPSEEK_API_KEY=$deepseek_key/" .env
        else
            echo "DEEPSEEK_API_KEY=$deepseek_key" >> .env
        fi
        
        echo "✓ DeepSeek 配置已保存"
        ;;
        
    2)
        echo ""
        echo "--- 支付宝沙盒配置 ---"
        echo "1. 访问 https://open.alipay.com"
        echo "2. 进入沙箱环境获取配置"
        echo ""
        read -p "请输入支付宝 APPID: " alipay_appid
        
        echo "请输入应用私钥（输入 END 结束）："
        private_key=""
        while IFS= read -r line; do
            [[ "$line" == "END" ]] && break
            private_key+="$line\\n"
        done
        
        # 更新 .env
        if grep -q "ALIPAY_APP_ID=" .env; then
            sed -i "s/ALIPAY_APP_ID=.*/ALIPAY_APP_ID=$alipay_appid/" .env
        else
            echo "ALIPAY_APP_ID=$alipay_appid" >> .env
        fi
        
        echo "✓ 支付宝配置已保存"
        echo "⚠️ 请手动将私钥写入 .env 文件的 ALIPAY_PRIVATE_KEY"
        ;;
        
    3)
        echo ""
        echo "--- 配置 DeepSeek AI ---"
        read -p "请输入 DeepSeek API Key: " deepseek_key
        
        if grep -q "DEEPSEEK_API_KEY=" .env; then
            sed -i "s/DEEPSEEK_API_KEY=.*/DEEPSEEK_API_KEY=$deepseek_key/" .env
        else
            echo "DEEPSEEK_API_KEY=$deepseek_key" >> .env
        fi
        
        echo "✓ DeepSeek 配置已保存"
        echo ""
        echo "--- 配置支付宝沙盒 ---"
        read -p "请输入支付宝 APPID: " alipay_appid
        
        if grep -q "ALIPAY_APP_ID=" .env; then
            sed -i "s/ALIPAY_APP_ID=.*/ALIPAY_APP_ID=$alipay_appid/" .env
        else
            echo "ALIPAY_APP_ID=$alipay_appid" >> .env
        fi
        
        echo "✓ 支付宝配置已保存"
        echo "⚠️ 请手动将私钥写入 .env 文件的 ALIPAY_PRIVATE_KEY"
        ;;
        
    4)
        echo "跳过配置"
        ;;
        
    *)
        echo "无效选项"
        exit 1
        ;;
esac

echo ""
echo "================================"
echo "配置完成！"
echo ""
echo "如需重启服务生效，请运行："
echo "  docker-compose restart backend"
echo "================================"
