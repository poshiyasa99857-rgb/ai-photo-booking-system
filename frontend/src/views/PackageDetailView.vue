<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { message } from 'ant-design-vue'
import { useUserStore } from '@/stores/user'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const packageId = route.params.id
const packageData = ref(null)
const loading = ref(false)
const bookingModalVisible = ref(false)

// 预约表单
const bookingForm = ref({
  booking_date: null,
  booking_time: null,
  photo_count: 0,
  retouch_count: 0,
  has_costume: false,
  contact_name: '',
  contact_phone: '',
  remark: '',
})

const fetchPackageDetail = async () => {
  loading.value = true
  try {
    const response = await axios.get(`/api/packages/packages/${packageId}/`)
    packageData.value = response.data
    
    // 初始化表单默认值
    bookingForm.value.photo_count = response.data.base_photo_count
    bookingForm.value.retouch_count = response.data.retouch_count
    bookingForm.value.has_costume = response.data.has_costume
  } catch (err) {
    message.error('获取套餐详情失败')
  } finally {
    loading.value = false
  }
}

const calculateTotal = () => {
  if (!packageData.value) return 0
  
  let total = parseFloat(packageData.value.current_price)
  
  // 额外底片费用
  const extraPhotos = Math.max(0, bookingForm.value.photo_count - packageData.value.base_photo_count)
  total += extraPhotos * 10
  
  // 额外精修费用
  const extraRetouch = Math.max(0, bookingForm.value.retouch_count - packageData.value.retouch_count)
  total += extraRetouch * 20
  
  // 服装妆造费用
  if (bookingForm.value.has_costume && !packageData.value.has_costume) {
    total += 100
  }
  
  return total
}

const showBookingModal = () => {
  if (!userStore.isLoggedIn) {
    message.warning('请先登录')
    router.push('/login')
    return
  }
  
  // 填充联系人信息
  if (userStore.user) {
    bookingForm.value.contact_name = userStore.user.username
    bookingForm.value.contact_phone = userStore.user.phone || ''
  }
  
  bookingModalVisible.value = true
}

const handleBooking = async () => {
  if (!bookingForm.value.booking_date || !bookingForm.value.booking_time) {
    message.error('请选择预约时间')
    return
  }
  
  try {
    const data = {
      package: packageId,
      booking_date: dayjs(bookingForm.value.booking_date).format('YYYY-MM-DD'),
      booking_time: dayjs(bookingForm.value.booking_time).format('HH:mm'),
      photo_count: bookingForm.value.photo_count,
      retouch_count: bookingForm.value.retouch_count,
      has_costume: bookingForm.value.has_costume,
      contact_name: bookingForm.value.contact_name,
      contact_phone: bookingForm.value.contact_phone,
      remark: bookingForm.value.remark,
    }
    
    const response = await axios.post('/api/bookings/bookings/', data)
    message.success('预约成功')
    bookingModalVisible.value = false
    
    // 跳转到支付页面
    router.push(`/payment/${response.data.id}`)
  } catch (err) {
    message.error('预约失败')
  }
}

const disabledDate = (current) => {
  // 不能选择今天之前的日期
  return current && current < dayjs().startOf('day')
}

onMounted(() => {
  fetchPackageDetail()
})
</script>

<template>
  <div class="package-detail-view">
    <a-spin :spinning="loading">
      <template v-if="packageData">
        <!-- 套餐基本信息 -->
        <a-row :gutter="24">
          <a-col :span="14">
            <a-carousel arrows dots-class="slick-dots slick-thumb">
              <div v-for="(img, index) in [packageData.cover_image, ...(packageData.sample_images || [])]" :key="index">
                <img :src="img" class="carousel-image" />
              </div>
            </a-carousel>
          </a-col>
          
          <a-col :span="10">
            <a-card class="info-card">
              <a-typography-title :level="3">{{ packageData.name }}</a-typography-title>
              
              <a-space class="tags">
                <a-tag v-for="tag in packageData.tags" :key="tag">{{ tag }}</a-tag>
              </a-space>
              
              <div class="price-section">
                <span class="current-price">¥{{ packageData.current_price }}</span>
                <span v-if="packageData.original_price > packageData.current_price" class="original-price">
                  ¥{{ packageData.original_price }}
                </span>
              </div>
              
              <a-descriptions :column="1" class="info-list">
                <a-descriptions-item label="底片数量">
                  {{ packageData.base_photo_count }}张
                </a-descriptions-item>
                <a-descriptions-item label="精修数量">
                  {{ packageData.retouch_count }}张
                </a-descriptions-item>
                <a-descriptions-item label="服装妆造">
                  {{ packageData.has_costume ? '包含' : '不包含' }}
                </a-descriptions-item>
                <a-descriptions-item label="拍摄时长">
                  {{ packageData.duration }}小时
                </a-descriptions-item>
                <a-descriptions-item label="拍摄地点">
                  {{ packageData.location }}
                </a-descriptions-item>
              </a-descriptions>
              
              <div class="stats">
                <span><EyeOutlined /> {{ packageData.view_count }}浏览</span>
                <span><ShoppingOutlined /> {{ packageData.booking_count }}预约</span>
              </div>
              
              <a-button
                type="primary"
                size="large"
                block
                class="booking-btn"
                @click="showBookingModal"
              >
                立即预约
              </a-button>
            </a-card>
          </a-col>
        </a-row>
        
        <!-- 套餐详情 -->
        <a-card title="套餐详情" class="detail-card">
          <a-typography-paragraph>
            {{ packageData.description }}
          </a-typography-paragraph>
          
          <a-divider v-if="packageData.ai_description" />
          
          <div v-if="packageData.ai_description">
            <h4>AI推荐描述</h4>
            <a-typography-paragraph type="secondary">
              {{ packageData.ai_description }}
            </a-typography-paragraph>
          </div>
        </a-card>
      </template>
    </a-spin>
    
    <!-- 预约弹窗 -->
    <a-modal
      v-model:visible="bookingModalVisible"
      title="预约套餐"
      width="600px"
      @ok="handleBooking"
    >
      <a-form :model="bookingForm" layout="vertical">
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="预约日期" required>
              <a-date-picker
                v-model:value="bookingForm.booking_date"
                style="width: 100%"
                :disabledDate="disabledDate"
              />
            </a-form-item>
          </a-col>
          
          <a-col :span="12">
            <a-form-item label="预约时间" required>
              <a-time-picker
                v-model:value="bookingForm.booking_time"
                style="width: 100%"
                format="HH:mm"
              />
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-row :gutter="16">
          <a-col :span="12">
            <a-form-item label="底片数量">
              <a-input-number
                v-model:value="bookingForm.photo_count"
                :min="0"
                :max="100"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
          
          <a-col :span="12">
            <a-form-item label="精修数量">
              <a-input-number
                v-model:value="bookingForm.retouch_count"
                :min="0"
                :max="10"
                style="width: 100%"
              />
            </a-form-item>
          </a-col>
        </a-row>
        
        <a-form-item>
          <a-checkbox v-model:checked="bookingForm.has_costume">需要服装妆造</a-checkbox>
        </a-form-item>
        
        <a-form-item label="联系人姓名" required>
          <a-input v-model:value="bookingForm.contact_name" />
        </a-form-item>
        
        <a-form-item label="联系人电话" required>
          <a-input v-model:value="bookingForm.contact_phone" />
        </a-form-item>
        
        <a-form-item label="备注">
          <a-textarea v-model:value="bookingForm.remark" rows="3" />
        </a-form-item>
        
        <a-divider />
        
        <div class="total-price">
          <span>总价：</span>
          <span class="price">¥{{ calculateTotal() }}</span>
          <span class="deposit">（定金：¥{{ (calculateTotal() * 0.3).toFixed(2) }}）</span>
        </div>
      </a-form>
    </a-modal>
  </div>
</template>

<style scoped>
.package-detail-view {
  max-width: 1200px;
  margin: 0 auto;
}

.carousel-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 8px;
}

.info-card {
  height: 100%;
}

.tags {
  margin-bottom: 16px;
}

.price-section {
  margin-bottom: 20px;
}

.current-price {
  color: #f5222d;
  font-size: 32px;
  font-weight: bold;
  margin-right: 12px;
}

.original-price {
  color: #999;
  text-decoration: line-through;
  font-size: 18px;
}

.info-list {
  margin-bottom: 20px;
}

.stats {
  display: flex;
  gap: 24px;
  margin-bottom: 20px;
  color: #666;
}

.booking-btn {
  margin-top: 20px;
}

.detail-card {
  margin-top: 24px;
}

.total-price {
  text-align: right;
  font-size: 16px;
}

.total-price .price {
  color: #f5222d;
  font-size: 24px;
  font-weight: bold;
  margin-left: 8px;
}

.total-price .deposit {
  color: #999;
  margin-left: 8px;
}
</style>
