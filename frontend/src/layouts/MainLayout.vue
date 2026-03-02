<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { message } from 'ant-design-vue'
import {
  HomeOutlined,
  CameraOutlined,
  RobotOutlined,
  MessageOutlined,
  UserOutlined,
  LogoutOutlined,
  BellOutlined,
} from '@ant-design/icons-vue'
import NotificationBell from '@/components/NotificationBell.vue'

const router = useRouter()
const userStore = useUserStore()

const selectedKeys = ref(['home'])

const menuItems = [
  { key: 'home', icon: HomeOutlined, label: '首页', path: '/' },
  { key: 'packages', icon: CameraOutlined, label: '套餐', path: '/packages' },
  { key: 'ai-chat', icon: RobotOutlined, label: 'AI助手', path: '/ai-chat' },
  { key: 'forum', icon: MessageOutlined, label: '论坛', path: '/forum' },
]

const userMenuItems = [
  { key: 'profile', icon: UserOutlined, label: '个人中心', path: '/profile' },
  { key: 'bookings', icon: CameraOutlined, label: '我的预约', path: '/bookings' },
  { key: 'feedback', icon: MessageOutlined, label: '意见反馈', path: '/feedback' },
]

const handleMenuClick = (item: any) => {
  const menuItem = menuItems.find(m => m.key === item.key)
  if (menuItem) {
    router.push(menuItem.path)
  }
}

const handleLogout = async () => {
  await userStore.logout()
  message.success('已退出登录')
  router.push('/login')
}

onMounted(() => {
  userStore.fetchProfile()
})
</script>

<template>
  <a-layout class="main-layout">
    <a-layout-header class="header">
      <div class="logo">
        <CameraOutlined />
        <span>AI摄影预约</span>
      </div>
      
      <a-menu
        theme="dark"
        mode="horizontal"
        v-model:selectedKeys="selectedKeys"
        :style="{ flex: 1, minWidth: 0 }"
        @click="handleMenuClick"
      >
        <a-menu-item v-for="item in menuItems" :key="item.key">
          <template #icon>
            <component :is="item.icon" />
          </template>
          {{ item.label }}
        </a-menu-item>
      </a-menu>
      
      <div class="user-actions">
        <template v-if="userStore.isLoggedIn">
          <NotificationBell style="margin-right: 16px" />
          <a-dropdown>
            <a-button type="text" style="color: white">
              <UserOutlined />
              {{ userStore.user?.username }}
            </a-button>
            <template #overlay>
              <a-menu>
                <a-menu-item v-for="item in userMenuItems" :key="item.key" @click="$router.push(item.path)">
                  <component :is="item.icon" /> {{ item.label }}
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item @click="handleLogout">
                  <LogoutOutlined /> 退出登录
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </template>
        <template v-else>
          <a-button type="primary" @click="$router.push('/login')">登录</a-button>
          <a-button @click="$router.push('/register')" style="margin-left: 8px">注册</a-button>
        </template>
      </div>
    </a-layout-header>
    
    <a-layout-content class="content">
      <router-view />
    </a-layout-content>
    
    <a-layout-footer class="footer">
      AI智能摄影预约系统 © 2024
    </a-layout-footer>
  </a-layout>
</template>

<style scoped>
.main-layout {
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  color: white;
  font-size: 18px;
  font-weight: bold;
  margin-right: 48px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.content {
  padding: 24px;
  background: #f0f2f5;
  min-height: calc(100vh - 64px - 70px);
}

.footer {
  text-align: center;
  background: #001529;
  color: rgba(255, 255, 255, 0.65);
}

.user-actions {
  margin-left: auto;
}
</style>
