<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const messages = ref([
  {
    role: 'assistant',
    content: '您好！我是AI摄影顾问，可以帮您了解套餐详情、推荐适合的拍摄方案，请问有什么可以帮您的？',
  },
])

const inputMessage = ref('')
const loading = ref(false)

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return
  
  const userMessage = inputMessage.value
  messages.value.push({ role: 'user', content: userMessage })
  inputMessage.value = ''
  loading.value = true
  
  try {
    const response = await axios.post('/api/ai/services/chat/', {
      message: userMessage,
      history: messages.value,
    })
    
    messages.value.push({
      role: 'assistant',
      content: response.data.reply,
    })
  } catch (err) {
    messages.value.push({
      role: 'assistant',
      content: '抱歉，AI服务暂时不可用，请稍后重试。',
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="ai-chat-view">
    <a-card title="AI智能客服" class="chat-card">
      <div class="chat-messages">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.role]"
        >
          <div class="message-content">
            <div class="message-avatar">
              <a-avatar
                :style="{
                  backgroundColor: msg.role === 'assistant' ? '#1890ff' : '#52c41a',
                }"
              >
                {{ msg.role === 'assistant' ? 'AI' : '我' }}
              </a-avatar>
            </div>
            <div class="message-text">
              {{ msg.content }}
            </div>
          </div>
        </div>
        
        <div v-if="loading" class="message assistant">
          <div class="message-content">
            <div class="message-avatar">
              <a-avatar style="background-color: #1890ff">AI</a-avatar>
            </div>
            <div class="message-text">
              <a-spin size="small" /> 思考中...
            </div>
          </div>
        </div>
      </div>
      
      <div class="chat-input">
        <a-input-group compact>
          <a-input
            v-model:value="inputMessage"
            placeholder="请输入您的问题..."
            size="large"
            @pressEnter="sendMessage"
            style="width: calc(100% - 100px)"
          />
          <a-button
            type="primary"
            size="large"
            :loading="loading"
            @click="sendMessage"
            style="width: 100px"
          >
            发送
          </a-button>
        </a-input-group>
      </div>
    </a-card>
  </div>
</template>

<style scoped>
.ai-chat-view {
  max-width: 900px;
  margin: 0 auto;
}

.chat-card {
  height: calc(100vh - 200px);
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #f5f5f5;
  border-radius: 8px;
  margin-bottom: 16px;
}

.message {
  margin-bottom: 16px;
}

.message-content {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.message.user .message-content {
  flex-direction: row-reverse;
}

.message-text {
  background: white;
  padding: 12px 16px;
  border-radius: 8px;
  max-width: 70%;
  word-wrap: break-word;
}

.message.user .message-text {
  background: #1890ff;
  color: white;
}

.chat-input {
  padding-top: 8px;
}
</style>
