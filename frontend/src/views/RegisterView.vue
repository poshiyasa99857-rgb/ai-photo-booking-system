<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { message } from 'ant-design-vue'

const router = useRouter()
const userStore = useUserStore()

const form = ref({
  username: '',
  email: '',
  phone: '',
  password: '',
  confirm_password: '',
})

const loading = ref(false)

const handleRegister = async () => {
  if (!form.value.username || !form.value.password) {
    message.error('请填写完整信息')
    return
  }
  
  if (form.value.password !== form.value.confirm_password) {
    message.error('两次密码不一致')
    return
  }
  
  loading.value = true
  try {
    await userStore.register(form.value)
    message.success('注册成功，请登录')
    router.push('/login')
  } catch (err: any) {
    message.error(userStore.error || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register-container">
    <a-card title="用户注册" class="register-card">
      <a-form :model="form" layout="vertical">
        <a-form-item label="用户名" required>
          <a-input
            v-model:value="form.username"
            placeholder="请输入用户名"
            size="large"
          />
        </a-form-item>
        
        <a-form-item label="邮箱">
          <a-input
            v-model:value="form.email"
            placeholder="请输入邮箱"
            size="large"
          />
        </a-form-item>
        
        <a-form-item label="手机号">
          <a-input
            v-model:value="form.phone"
            placeholder="请输入手机号"
            size="large"
          />
        </a-form-item>
        
        <a-form-item label="密码" required>
          <a-input-password
            v-model:value="form.password"
            placeholder="请输入密码"
            size="large"
          />
        </a-form-item>
        
        <a-form-item label="确认密码" required>
          <a-input-password
            v-model:value="form.confirm_password"
            placeholder="请再次输入密码"
            size="large"
          />
        </a-form-item>
        
        <a-form-item>
          <a-button
            type="primary"
            size="large"
            block
            :loading="loading"
            @click="handleRegister"
          >
            注册
          </a-button>
        </a-form-item>
        
        <a-form-item>
          <a-button type="link" @click="$router.push('/login')">
            已有账号？立即登录
          </a-button>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.register-card {
  width: 400px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}
</style>
