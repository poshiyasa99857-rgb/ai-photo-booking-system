# AI 智能摄影预约系统

基于 Django + Vue3 + DeepSeek AI 的摄影预约管理系统

## ✅ 功能完整性

本项目已实现图中所有功能模块：

### 前端用户模块 (10/10) ✅
- [x] 注册登录模块
- [x] 首页展示模块
- [x] 套餐浏览模块
- [x] AI智能推荐模块
- [x] 预约管理模块
- [x] 用户中心模块
- [x] 论坛讨论模块
- [x] 支付模块
- [x] 搜索模块
- [x] AI智能客服

### 后端管理模块 (10/10) ✅
- [x] 用户管理
- [x] 套餐管理
- [x] 预约管理
- [x] 分类管理
- [x] 论坛管理
- [x] 日志管理
- [x] 统计分析
- [x] 系统配置
- [x] 意见反馈
- [x] AI服务管理

## 🚀 快速开始

### 方式1：Docker 一键启动（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/poshiyasa99857-rgb/ai-photo-booking-system.git
cd ai-photo-booking-system

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置数据库密码

# 3. 启动所有服务
docker-compose up -d

# 4. 等待初始化完成（约30秒）
docker-compose logs -f backend

# 5. 访问
# 前端: http://localhost
# 后端 API: http://localhost:8000/api/
# 管理后台: http://localhost:8000/admin/
```

### 方式2：本地开发

**后端：**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 创建数据库
createdb photo_booking  # 或使用MySQL

# 配置环境变量
cp .env.example .env
# 编辑 .env

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
npm install
npm run dev
```

## ⚙️ 环境变量配置

复制 `.env.example` 为 `.env` 并填写：

```env
# 必填：数据库配置
DB_PASSWORD=your_mysql_password

# 可选：DeepSeek AI（用于AI功能）
# 获取地址：https://platform.deepseek.com
DEEPSEEK_API_KEY=your_api_key

# 可选：支付宝沙盒（用于支付功能）
# 获取地址：https://open.alipay.com/develop/sandbox
ALIPAY_APP_ID=your_app_id
ALIPAY_PRIVATE_KEY=your_private_key
```

## 🔑 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 超级管理员 | admin | admin123 |

## 📁 项目结构

```
ai-photo-booking-system/
├── backend/                  # Django 后端
│   ├── apps/
│   │   ├── users/           # 用户管理 + 通知
│   │   ├── packages/        # 套餐管理 + AI描述
│   │   ├── bookings/        # 预约管理 + AI建议
│   │   ├── forum/           # 论坛模块
│   │   ├── payments/        # 支付模块
│   │   ├── ai_services/     # DeepSeek AI
│   │   └── analytics/       # 统计分析 + 反馈
│   └── config/
├── frontend/                 # Vue 前端
│   ├── src/
│   │   ├── views/           # 页面
│   │   ├── components/      # 组件
│   │   └── stores/          # 状态管理
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 🔧 功能测试清单

### 用户功能
- [ ] 注册新账号
- [ ] 登录/退出
- [ ] 浏览套餐列表
- [ ] 查看套餐详情
- [ ] 使用AI客服咨询
- [ ] 创建预约
- [ ] 支付定金
- [ ] 查看我的预约
- [ ] 发表论坛帖子
- [ ] 提交意见反馈

### 管理功能
- [ ] 登录管理后台
- [ ] 管理用户账号
- [ ] 添加/编辑套餐
- [ ] 使用AI生成套餐描述
- [ ] 处理预约订单
- [ ] 管理论坛内容
- [ ] 查看统计数据
- [ ] 回复用户反馈

## 🐳 Docker 常用命令

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# 停止服务
docker-compose down

# 重建镜像
docker-compose up -d --build

# 进入容器
docker-compose exec backend bash
docker-compose exec db mysql -uroot -p

# 数据库迁移
docker-compose exec backend python manage.py migrate

# 创建超级管理员
docker-compose exec backend python manage.py createsuperuser
```

## ⚠️ 常见问题

### 1. 数据库连接失败
**解决：** 检查 `.env` 中的 `DB_PASSWORD` 是否正确，确保MySQL容器已启动

### 2. AI功能无法使用
**解决：** 需要配置 `DEEPSEEK_API_KEY`，否则AI功能会返回提示信息

### 3. 前端无法连接后端
**解决：** 检查 `docker-compose.yml` 中的服务名和网络配置

### 4. 静态文件无法加载
**解决：** 运行 `docker-compose exec backend python manage.py collectstatic`

## 📝 开发计划

- [x] 核心功能开发
- [x] Docker部署
- [ ] 微信小程序
- [ ] 短信验证码
- [ ] 邮件通知
- [ ] 文件上传OSS

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
