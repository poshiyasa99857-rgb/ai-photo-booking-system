<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import axios from 'axios'
import { message } from 'ant-design-vue'

const userStore = useUserStore()
const activeKey = ref('profile')

const profileForm = ref({
  username: '',
  email: '',
  phone: '',
  gender: '',
  birthday: null,
  address: '',
})

const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: '',
})

const favorites = ref([])
const reviews = ref([])

const fetchProfile = () => {
  if (userStore.user) {
    profileForm.value = { ...userStore.user }
  }
}

const updateProfile = async () => {
  try {
    await axios.put('/api/users/update_profile/', profileForm.value)
    message.success('更新成功')
    userStore.fetchProfile()
  } catch (err) {
    message.error('更新失败')
  }
}

const changePassword = async () => {
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    message.error('两次密码不一致')
    return
  }
  
  try {
    await axios.post('/api/users/change_password/', passwordForm.value)
    message.success('密码修改成功')
    passwordForm.value = { old_password: '', new_password: '', confirm_password: '' }
  } catch (err) {
    message.error('密码修改失败')
  }
}

const fetchFavorites = async () => {
  try {
    const response = await axios.get('/api/users/favorites/')
    favorites.value = response.data.results || []
  } catch (err) {
    console.error('获取收藏失败', err)
  }
}

const fetchReviews = async () => {
  try {
    const response = await axios.get('/api/users/reviews/')
    reviews.value = response.data.results || []
  } catch (err) {
    console.error('获取评价失败', err)
  }
}

const removeFavorite = async (id) => {
  try {
    await axios.delete(`/api/users/favorites/${id}/`)
    message.success('取消收藏')
    fetchFavorites()
  } catch (err) {
    message.error('操作失败')
  }
}

const deleteReview = async (id) => {
  try {
    await axios.delete(`/api/users/reviews/${id}/`)
    message.success('删除成功')
    fetchReviews()
  } catch (err) {
    message.error('删除失败')
  }
}

onMounted(() => {
  fetchProfile()
  fetchFavorites()
  fetchReviews()
})
</script>

<template>
  <div class="profile-view">
    <a-tabs v-model:activeKey="activeKey">
      <!-- 基本资料 -->
      <a-tab-pane key="profile" tab="基本资料">
        <a-card title="个人信息">
          <a-form :model="profileForm" layout="vertical">
            <a-form-item label="用户名">
              <a-input v-model:value="profileForm.username" disabled />
            </a-form-item>
            
            <a-form-item label="邮箱">
              <a-input v-model:value="profileForm.email" />
            </a-form-item>
            
            <a-form-item label="手机号">
              <a-input v-model:value="profileForm.phone" />
            </a-form-item>
            
            <a-form-item label="性别">
              <a-select v-model:value="profileForm.gender">
                <a-select-option value="male">男</a-select-option>
                <a-select-option value="female">女</a-select-option>
                <a-select-option value="other">其他</a-select-option>
              </a-select>
            </a-form-item>
            
            <a-form-item label="地址">
              <a-textarea v-model:value="profileForm.address" rows="3" />
            </a-form-item>
            
            <a-form-item>
              <a-button type="primary" @click="updateProfile">保存修改</a-button>
            </a-form-item>
          </a-form>
        </a-card>
      </a-tab-pane>
      
      <!-- 修改密码 -->
      <a-tab-pane key="password" tab="修改密码">
        <a-card title="修改密码">
          <a-form :model="passwordForm" layout="vertical">
            <a-form-item label="原密码">
              <a-input-password v-model:value="passwordForm.old_password" />
            </a-form-item>
            
            <a-form-item label="新密码">
              <a-input-password v-model:value="passwordForm.new_password" />
            </a-form-item>
            
            <a-form-item label="确认新密码">
              <a-input-password v-model:value="passwordForm.confirm_password" />
            </a-form-item>
            
            <a-form-item>
              <a-button type="primary" @click="changePassword">修改密码</a-button>
            </a-form-item>
          </a-form>
        </a-card>
      </a-tab-pane>
      
      <!-- 我的收藏 -->
      <a-tab-pane key="favorites" tab="我的收藏">
        <a-card title="收藏的套餐">
          <a-list :data-source="favorites">
            <template #renderItem="{ item }">
              <a-list-item>
                <a-list-item-meta
                  :title="item.package_name"
                  :description="`收藏时间：${item.created_at}`"
                >
                  <template #avatar>
                    <a-avatar shape="square" :src="item.package_image" />
                  </template>
                </a-list-item-meta>
                
                <a-button type="link" danger @click="removeFavorite(item.id)"
                  取消收藏</a-button>
              </a-list-item>
            </template>
            
            <a-empty v-if="favorites.length === 0" description="暂无收藏" />
          </a-list>
        </a-card>
      </a-tab-pane>
      
      <!-- 我的评价 -->
      <a-tab-pane key="reviews" tab="我的评价">
        <a-card title="历史评价">
          <a-list :data-source="reviews">
            <template #renderItem="{ item }">
              <a-list-item>
                <a-list-item-meta
                  :title="`评分：${item.rating}星`"
                  :description="item.content"
                >
                </a-list-item-meta>
                
                <a-space>
                  <span>{{ item.created_at }}</span>
                  <a-button type="link" danger @click="deleteReview(item.id)"
                    删除</a-button>
                </a-space>
              </a-list-item>
            </template>
            
            <a-empty v-if="reviews.length === 0" description="暂无评价" />
          </a-list>
        </a-card>
      </a-tab-pane>
    </a-tabs>
  </div>
</template>

<style scoped>
.profile-view {
  max-width: 800px;
  margin: 0 auto;
}
</style>
