<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import axios from 'axios'
import { message } from 'ant-design-vue'

const userStore = useUserStore()
const activeKey = ref('create')

// 创建反馈
const feedbackForm = ref({
  type: 'suggestion',
  title: '',
  content: '',
  contact_info: '',
  images: [],
})

// 我的反馈列表
const myFeedbacks = ref([])
const loading = ref(false)

const feedbackTypes = [
  { value: 'complaint', label: '投诉' },
  { value: 'suggestion', label: '建议' },
  { value: 'consultation', label: '咨询' },
  { value: 'other', label: '其他' },
]

const statusMap = {
  'pending': { text: '待处理', color: 'orange' },
  'processing': { text: '处理中', color: 'blue' },
  'resolved': { text: '已解决', color: 'green' },
  'closed': { text: '已关闭', color: 'default' },
}

const submitFeedback = async () => {
  if (!feedbackForm.value.title || !feedbackForm.value.content) {
    message.error('请填写完整信息')
    return
  }
  
  try {
    await axios.post('/api/analytics/feedbacks/', feedbackForm.value)
    message.success('提交成功')
    feedbackForm.value = {
      type: 'suggestion',
      title: '',
      content: '',
      contact_info: '',
      images: [],
    }
    activeKey.value = 'list'
    fetchMyFeedbacks()
  } catch (err) {
    message.error('提交失败')
  }
}

const fetchMyFeedbacks = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/analytics/feedbacks/')
    myFeedbacks.value = response.data.results || []
  } catch (err) {
    console.error('获取反馈列表失败', err)
  } finally {
    loading.value = false
  }
}

const rateFeedback = async (id, rating) => {
  try {
    await axios.post(`/api/analytics/feedbacks/${id}/rate/`, { satisfaction: rating })
    message.success('评价成功')
    fetchMyFeedbacks()
  } catch (err) {
    message.error('评价失败')
  }
}

onMounted(() => {
  fetchMyFeedbacks()
})
</script>

<template>
  <div class="feedback-view">
    <a-tabs v-model:activeKey="activeKey">
      <!-- 提交反馈 -->
      <a-tab-pane key="create" tab="提交反馈">
        <a-card title="意见反馈">
          <a-form :model="feedbackForm" layout="vertical">
            <a-form-item label="反馈类型" required>
              <a-radio-group v-model:value="feedbackForm.type">
                <a-radio-button v-for="t in feedbackTypes" :key="t.value" :value="t.value"
                  {{ t.label }}
                </a-radio-button>
              </a-radio-group>
            </a-form-item>
            
            <a-form-item label="标题" required>
              <a-input
                v-model:value="feedbackForm.title"
                placeholder="请简要描述您的问题或建议"
                maxlength="100"
                show-count
              />
            </a-form-item>
            
            <a-form-item label="详细内容" required>
              <a-textarea
                v-model:value="feedbackForm.content"
                placeholder="请详细描述您遇到的问题或建议..."
                rows="6"
                maxlength="1000"
                show-count
              />
            </a-form-item>
            
            <a-form-item label="联系方式">
              <a-input
                v-model:value="feedbackForm.contact_info"
                placeholder="手机/邮箱/微信（选填，方便我们联系您）"
              />
            </a-form-item>
            
            <a-form-item>
              <a-button type="primary" size="large" @click="submitFeedback"
                提交反馈
              </a-button>
            </a-form-item>
          </a-form>
        </a-card>
      </a-tab-pane>
      
      <!-- 我的反馈 -->
      <a-tab-pane key="list" tab="我的反馈">
        <a-card title="反馈记录" :loading="loading">
          <a-list :data-source="myFeedbacks">
            <template #renderItem="{ item }">
              <a-list-item class="feedback-item">
                <a-list-item-meta
                  :title="item.title"
                  :description="item.content"
                >
                  <template #avatar>
                    <a-avatar :style="{ backgroundColor: '#1890ff' }"
                      {{ item.type_display[0] }}
                    </a-avatar>
                  </template>
                </a-list-item-meta>
                
                <div class="feedback-meta">
                  <a-space>
                    <a-tag :color="statusMap[item.status].color"
                      {{ statusMap[item.status].text }}
                    </a-tag>
                    <span>{{ item.created_at }}</span>
                  </a-space>
                </div>
                
                <!-- 管理员回复 -->
                <div v-if="item.reply" class="reply-section">
                  <a-divider />
                  <div class="reply-content">
                    <strong>管理员回复：</strong>
                    <p>{{ item.reply }}</p>
                    <span class="reply-time">{{ item.replied_at }}</span>
                  </div>
                  
                  <!-- 满意度评价 -->
                  <div v-if="item.status === 'resolved' && !item.satisfaction" class="rating-section">
                    <p>请对处理结果进行评价：</p>
                    <a-rate @change="(val) => rateFeedback(item.id, val)" />
                  </div>
                  
                  <div v-if="item.satisfaction" class="satisfaction">
                    您的评价：<a-rate :value="item.satisfaction" disabled />
                  </div>
                </div>
              </a-list-item>
            </template>
            
            <a-empty v-if="!loading && myFeedbacks.length === 0" description="暂无反馈记录" />
          </a-list>
        </a-card>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<style scoped>
.feedback-view {
  max-width: 800px;
  margin: 0 auto;
}

.feedback-item {
  padding: 20px;
}

.feedback-meta {
  margin-top: 12px;
}

.reply-section {
  margin-top: 16px;
  padding: 16px;
  background: #f6ffed;
  border-radius: 8px;
}

.reply-content {
  color: #333;
}

.reply-time {
  color: #999;
  font-size: 12px;
}

.rating-section {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #d9d9d9;
}

.satisfaction {
  margin-top: 12px;
  color: #666;
}
</style>
