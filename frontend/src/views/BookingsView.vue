<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { message } from 'ant-design-vue'
import dayjs from 'dayjs'

const router = useRouter()

const bookings = ref([])
const loading = ref(false)

const fetchBookings = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/bookings/bookings/')
    bookings.value = response.data.results || []
  } catch (err) {
    message.error('获取预约失败')
  } finally {
    loading.value = false
  }
}

const getStatusText = (status) => {
  const statusMap = {
    'pending': '待确认',
    'confirmed': '已确认',
    'completed': '已完成',
    'cancelled': '已取消',
  }
  return statusMap[status] || status
}

const getStatusColor = (status) => {
  const colorMap = {
    'pending': 'orange',
    'confirmed': 'blue',
    'completed': 'green',
    'cancelled': 'red',
  }
  return colorMap[status] || 'default'
}

const cancelBooking = async (id) => {
  try {
    await axios.post(`/api/bookings/bookings/${id}/cancel/`)
    message.success('预约已取消')
    fetchBookings()
  } catch (err) {
    message.error('取消失败')
  }
}

const payBooking = async (id) => {
  router.push(`/payment/${id}`)
}

const viewDetail = (id) => {
  router.push(`/booking/${id}`)
}

onMounted(() => {
  fetchBookings()
})
</script>

<template>
  <div class="bookings-view">
    <a-card title="我的预约">
      <a-list :data-source="bookings" :loading="loading">
        <template #renderItem="{ item }">
          <a-list-item class="booking-item">
            <a-list-item-meta
              :title="item.package_name"
              :description="`预约时间：${item.booking_date} ${item.booking_time}`"
            >
              <template #avatar>
                <a-avatar shape="square" :src="item.package_image" />
              </template>
            </a-list-item-meta>
            
            <div class="booking-info">
              <div class="info-row">
                <span>摄影师：{{ item.photographer_name || '待定' }}</span>
                <span>总价：<strong>¥{{ item.total_price }}</strong></span>
              </div>
              
              <div class="info-row">
                <a-tag :color="getStatusColor(item.status)">
                  {{ getStatusText(item.status) }}
                </a-tag>
                
                <a-tag v-if="item.is_paid" color="green">已支付</a-tag>
                <a-tag v-else color="orange">待支付</a-tag>
              </div>
              
              <div class="actions">
                <a-button type="link" @click="viewDetail(item.id)"
                  查看详情</a-button>
                
                <a-button
                  v-if="!item.is_paid && item.status !== 'cancelled'"
                  type="primary"
                  size="small"
                  @click="payBooking(item.id)"
                >
                  支付定金
                </a-button>
                
                <a-button
                  v-if="item.status === 'pending'"
                  danger
                  size="small"
                  @click="cancelBooking(item.id)"
                >
                  取消
                </a-button>
              </div>
            </div>
          </a-list-item>
        </template>
        
        <a-empty v-if="!loading && bookings.length === 0" description="暂无预约" />
      </a-list>
    </a-card>
  </div>
</template>

<style scoped>
.bookings-view {
  max-width: 900px;
  margin: 0 auto;
}

.booking-item {
  padding: 20px;
}

.booking-info {
  margin-top: 12px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}
</style>
