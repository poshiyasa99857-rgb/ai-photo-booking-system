# AI和支付配置指南

## 🤖 DeepSeek AI 配置（推荐配置）

### 为什么需要？
- AI智能客服（7×24小时自动回复）
- AI套餐描述生成（自动生成营销文案）
- AI拍摄建议（预约后自动生成拍摄指南）
- AI智能推荐（根据用户需求推荐套餐）

### 配置步骤

**Step 1: 获取 API Key**
```
1. 访问 https://platform.deepseek.com
2. 用手机号注册账号
3. 登录后点击左侧「API Keys」
4. 点击「创建 API Key」
5. 复制 Key（格式：sk-xxxxxxxxxx）
```

**Step 2: 配置到项目**
```bash
# 方法1：直接编辑 .env
echo "DEEPSEEK_API_KEY=sk-your-key-here" >> .env

# 方法2：使用配置脚本
./setup_config.sh
# 选择选项 1

# 重启服务
docker-compose restart backend
```

**Step 3: 验证**
- 访问 AI客服页面，发送消息测试
- 创建预约，查看是否生成拍摄建议

### 费用说明
- 新用户免费额度：**5000万 Token**
- 按量付费：约 ¥2/百万 Token
- 个人项目完全够用

---

## 💰 支付宝沙盒配置（可选）

### 为什么需要？
- 在线支付定金
- 模拟真实支付流程
- 测试支付回调

### 配置步骤

**Step 1: 获取沙盒配置**
```
1. 访问 https://open.alipay.com
2. 用支付宝账号登录
3. 点击「控制台」
4. 点击「沙箱」进入沙箱环境
5. 记录以下信息：
   - APPID（如：2024xxxxxxxxxxxx）
   - 支付宝公钥
   - 应用私钥
```

**Step 2: 配置到项目**
```bash
# 编辑 .env 文件
nano .env

# 添加以下内容
ALIPAY_APP_ID=2024xxxxxxxxxxxx
ALIPAY_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
-----END RSA PRIVATE KEY-----
ALIPAY_PUBLIC_KEY=-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...
-----END PUBLIC KEY-----

# 重启服务
docker-compose restart backend
```

**Step 3: 下载沙盒APP测试**
```
1. 在沙箱页面下载「支付宝沙盒APP」
2. 使用沙箱买家账号登录
3. 在网站创建预约并支付
4. 用沙盒APP扫码支付
```

### 沙盒账号信息
- 买家账号：在沙箱页面查看
- 登录密码：在沙箱页面查看
- 支付密码：在沙箱页面查看

---

## 📝 配置文件示例

完整的 `.env` 文件示例：

```env
# Django配置
DEBUG=True
SECRET_KEY=your-secret-key-here

# 数据库配置（必填）
DB_NAME=photo_booking
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=db
DB_PORT=3306

# DeepSeek AI配置（可选，推荐配置）
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# 支付宝沙盒配置（可选）
ALIPAY_APP_ID=2024xxxxxxxxxxxx
ALIPAY_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
-----END RSA PRIVATE KEY-----
ALIPAY_PUBLIC_KEY=-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8Axxxxxxxx
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
-----END PUBLIC KEY-----

# CORS配置
CORS_ALLOWED_ORIGINS=http://localhost,http://localhost:80
```

---

## ❓ 常见问题

### Q: 不配置这些功能能用吗？
**A:** 完全可以！
- 不配置 AI：系统会返回提示信息，其他功能正常
- 不配置支付：可以创建预约，但无法在线支付

### Q: DeepSeek API Key 安全吗？
**A:** 
- 只在后端使用，前端无法获取
- 建议定期更换
- 不要提交到 GitHub

### Q: 支付宝配置好就能收真实款项吗？
**A:** 不能！沙盒环境只能用于测试，真实收款需要：
1. 企业资质认证
2. 申请正式接口权限
3. 配置正式环境

### Q: 配置后需要重启吗？
**A:** 需要！修改 `.env` 后必须重启：
```bash
docker-compose restart backend
```

---

## 🚀 快速配置命令

```bash
# 1. 进入项目目录
cd ai-photo-booking-system

# 2. 运行配置脚本
./setup_config.sh

# 3. 按提示输入配置

# 4. 重启服务
docker-compose restart backend
```
