# AI 智能摄影预约系统

基于 Django + Vue3 + DeepSeek AI 的摄影预约管理系统

## 功能特性

### 前端用户模块
- ✅ 注册登录（支持手机号、邮箱、第三方登录）
- ✅ 首页展示（服务分类、热门套餐、优惠活动）
- ✅ 套餐浏览（详情、价格、参数配置）
- ✅ AI 智能推荐（自然语言需求匹配）
- ✅ 预约管理（日历选时、摄影师匹配）
- ✅ 用户中心（资料、订单、收藏、评价）
- ✅ 论坛讨论（帖子、回复、互动）
- ✅ 支付模块（支付宝沙盒）
- ✅ AI 智能客服（DeepSeek 7×24小时）

### 后端管理模块
- ✅ 用户管理
- ✅ 套餐管理（含 AI 描述生成）
- ✅ 预约管理
- ✅ 分类管理
- ✅ 论坛管理
- ✅ 日志管理
- ✅ 统计分析
- ✅ 系统配置
- ✅ 意见反馈
- ✅ AI 服务管理

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Django 4.2 + Django REST Framework |
| 前端 | Vue 3 + Vite + Ant Design Vue |
| 数据库 | MySQL 8.0 |
| AI | DeepSeek API |
| 部署 | Docker + Docker Compose |

## 快速开始

### 方式1：Docker 一键启动（推荐）

```bash
# 克隆项目
git clone https://github.com/yourusername/ai-photo-booking-system.git
cd ai-photo-booking-system

# 启动所有服务
docker-compose up -d

# 访问
# 前端: http://localhost:80
# 后端: http://localhost:8000
# 管理后台: http://localhost:8000/admin
```

### 方式2：本地开发

**后端：**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**前端：**
```bash
cd frontend
npm install
npm run dev
```

## 环境变量配置

复制 `.env.example` 为 `.env` 并填写：

```env
# 数据库
DB_NAME=photo_booking
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# DeepSeek AI
DEEPSEEK_API_KEY=your_api_key

# 支付宝沙盒
ALIPAY_APP_ID=your_app_id
ALIPAY_PRIVATE_KEY=your_private_key
```

## 项目结构

```
ai-photo-booking-system/
├── backend/              # Django 后端
│   ├── apps/            # 应用模块
│   ├── config/          # 项目配置
│   └── requirements.txt
├── frontend/            # Vue 前端
│   ├── src/
│   └── package.json
├── docker-compose.yml   # Docker 编排
├── Dockerfile.backend   # 后端镜像
├── Dockerfile.frontend  # 前端镜像
└── .github/workflows/   # CI/CD
```

## 部署

项目已配置 GitHub Actions，推送到 main 分支自动部署到 Railway。

## 许可证

MIT License
