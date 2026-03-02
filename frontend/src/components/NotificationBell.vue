<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { message } from 'ant-design-vue'

const visible = ref(false)
const notifications = ref([])
const unreadCount = ref(0)
const loading = ref(false)

const fetchNotifications = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/users/notifications/')
    notifications.value = response.data.results || []
  } catch (err) {
    console.error('获取通知失败', err)
  } finally {
    loading.value = false
  }
}

const fetchUnreadCount = async () => {
  try {
    const response = await axios.get('/api/users/notifications/unread/')
    unreadCount.value = response.data.count
  } catch (err) {
    console.error('获取未读数失败', err)
  }
}

const markAsRead = async (id) => {
  try {
    await axios.post(`/api/users/notifications/${id}/mark_read/`)
    fetchNotifications()
    fetchUnreadCount()
  } catch (err) {
    message.error('标记失败')
  }
}

const markAllAsRead = async () => {
  try {
    await axios.post('/api/users/notifications/mark_all_read/')
    message.success('全部已读')
    fetchNotifications()
    fetchUnreadCount()
  } catch (err) {
    message.error('操作失败')
  }
}

const getNotificationIcon = (type) => {
  const iconMap = {
    'system': '🔔',
    'booking': '📅',
    'payment': '💰',
    'ai_guide': '🤖',
    'forum': '💬',
  }
  return iconMap[type] || '📢'
}

const getNotificationColor = (type) => {
  const colorMap = {
    'system': 'blue',
    'booking': 'green',
    'payment': 'orange',
    'ai_guide': 'purple',
    'forum': 'cyan',
  }
  return colorMap[type] || 'default'
}

onMounted(() => {
  fetchUnreadCount()
})
</script>

<template>
  <a-dropdown v-model:visible="visible" trigger="click">
    <a-badge :count="unreadCount" :offset="[-2, 2]">
      <a-button type="text" @click="fetchNotifications">
        <BellOutlined />
      </a-button>
    </a-badge>
    
    <template #overlay>
      <a-card
        title="消息通知"
        style="width: 360px"
        :bodyStyle="{ padding: 0, maxHeight: '400px', overflow: 'auto' }"
      >
        <template #extra>
          <a-button type="link" size="small" @click="markAllAsRead"
            全部已读
          </a-button>
        </template>
        
        <a-list :data-source="notifications" :loading="loading">
          <template #renderItem="{ item }">
            <a-list-item
              :class="['notification-item', { unread: !item.is_read }]"
              @click="markAsRead(item.id)"
            >
              <a-list-item-meta
                :title="item.title"
                :description="item.content"
              >
                <template #avatar>
                  <a-avatar :style="{ backgroundColor: getNotificationColor(item.type) }"
                    {{ getNotificationIcon(item.type) }}
                  </a-avatar>
                </template>
              </a-list-item-meta>
              
              <div class="notification-time">
                {{ item.created_at }}
                <a-badge v-if="!item.is_read" status="processing" />
              </div>
            </a-list-item>
          </template>
          
          <a-empty
            v-if="!loading && notifications.length === 0"
            description="暂无通知"
            style="padding: 32px"
          />
        </a-list>
      </a-card>
    </template>
  </a-dropdown>
</template>

<style scoped>
.notification-item {
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.notification-item:hover {
  background-color: #f5f5f5;
}

.notification-item.unread {
  background-color: #e6f7ff;
}

.notification-time {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}
</style>
