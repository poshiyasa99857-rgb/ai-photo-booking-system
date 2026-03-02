# AI 智能摄影预约系统

基于 Django + Vue3 + DeepSeek AI 的摄影预约管理系统

## ✨ 功能特性

### 前端用户模块
- ✅ 注册登录（支持手机号、邮箱）
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
- ✅ AI 服务管理

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Django 4.2 + Django REST Framework |
| 前端 | Vue 3 + Vite + Ant Design Vue |
| 数据库 | MySQL 8.0 |
| AI | DeepSeek API |
| 部署 | Docker + Docker Compose |

## 🚀 快速开始

### 方式1：Docker 一键启动（推荐）

```bash
# 克隆项目
git clone https://github.com/poshiyasa99857-rgb/ai-photo-booking-system.git
cd ai-photo-booking-system

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置数据库密码等

# 启动所有服务
docker-compose up -d

# 等待数据库初始化完成（约30秒）

# 访问
# 前端: http://localhost
# 后端 API: http://localhost:8000/api/
# 管理后台: http://localhost:8000/admin/
```

### 方式2：本地开发

**后端：**
```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置数据库（MySQL）
# 创建数据库: CREATE DATABASE photo_booking CHARACTER SET utf8mb4;

# 复制环境变量
cp .env.example .env
# 编辑 .env 配置数据库连接

# 数据库迁移
python manage.py migrate

# 初始化数据
python ../init_database.py

# 启动服务
python manage.py runserver
```

**前端：**
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问 http://localhost:5173
```

## 📁 项目结构

```
ai-photo-booking-system/
├── backend/                  # Django 后端
│   ├── apps/
│   │   ├── users/           # 用户管理
│   │   ├── packages/        # 套餐管理
│   │   ├── bookings/        # 预约管理
│   │   ├── forum/           # 论坛模块
│   │   ├── payments/        # 支付模块
│   │   ├── ai_services/     # AI服务
│   │   └── analytics/       # 统计分析
│   ├── config/              # 项目配置
│   └── requirements.txt
├── frontend/                 # Vue 前端
│   ├── src/
│   │   ├── views/           # 页面
│   │   ├── components/      # 组件
│   │   ├── stores/          # Pinia状态管理
│   │   └── router/          # 路由
│   └── package.json
├── docker-compose.yml        # Docker 编排
├── Dockerfile.backend        # 后端镜像
├── Dockerfile.frontend       # 前端镜像
├── init_database.py          # 数据库初始化
└── README.md
```

## ⚙️ 环境变量配置

复制 `.env.example` 为 `.env` 并填写：

```env
# 数据库（必填）
DB_PASSWORD=your_mysql_password

# DeepSeek AI（可选，用于AI功能）
DEEPSEEK_API_KEY=your_api_key

# 支付宝沙盒（可选，用于支付功能）
ALIPAY_APP_ID=your_app_id
ALIPAY_PRIVATE_KEY=your_private_key
```

## 🔧 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 超级管理员 | admin | admin123 |

## 📚 API 文档

启动后端后访问：
- API 根: http://localhost:8000/api/
- 管理后台: http://localhost:8000/admin/

## 🐳 Docker 命令

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 停止服务
docker-compose down

# 重建镜像
docker-compose up -d --build

# 进入容器
docker-compose exec backend bash
docker-compose exec db mysql -uroot -p
```

## 📝 开发计划

- [x] 用户系统
- [x] 套餐管理
- [x] 预约系统
- [x] AI 智能客服
- [x] AI 智能推荐
- [x] 论坛模块
- [x] 支付系统
- [x] 管理后台
- [ ] 微信小程序
- [ ] 短信验证码
- [ ] 邮件通知

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系

如有问题，请在 GitHub 提交 Issue。
