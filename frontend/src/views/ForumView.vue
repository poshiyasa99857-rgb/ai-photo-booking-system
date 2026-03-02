<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { message } from 'ant-design-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const categories = ref([])
const posts = ref([])
const loading = ref(false)
const selectedCategory = ref(null)

const fetchCategories = async () => {
  try {
    const response = await axios.get('/api/forum/categories/')
    categories.value = response.data.results || response.data
  } catch (err) {
    console.error('获取分类失败', err)
  }
}

const fetchPosts = async (categoryId = null) => {
  loading.value = true
  try {
    const url = categoryId 
      ? `/api/forum/posts/?category=${categoryId}`
      : '/api/forum/posts/'
    const response = await axios.get(url)
    posts.value = response.data.results || []
  } catch (err) {
    console.error('获取帖子失败', err)
  } finally {
    loading.value = false
  }
}

const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
  fetchPosts(categoryId)
}

const goToPost = (postId) => {
  router.push(`/forum/post/${postId}`)
}

const createPost = () => {
  if (!userStore.isLoggedIn) {
    message.warning('请先登录')
    router.push('/login')
    return
  }
  router.push('/forum/create')
}

onMounted(() => {
  fetchCategories()
  fetchPosts()
})
</script>

<template>
  <div class="forum-view">
    <a-row :gutter="24">
      <!-- 左侧分类 -->
      <a-col :span="6">
        <a-card title="论坛分类">
          <a-menu
            mode="inline"
            :selectedKeys="[selectedCategory]"
            @click="({ key }) => selectCategory(key)"
          >
            <a-menu-item :key="null">
              <MessageOutlined /> 全部帖子
            </a-menu-item>
            <a-menu-item v-for="cat in categories" :key="cat.id">
              {{ cat.name }}
            </a-menu-item>
          </a-menu>
        </a-card>
      </a-col>
      
      <!-- 右侧帖子列表 -->
      <a-col :span="18">
        <a-card
          title="论坛讨论"
          :extra="<a-button type='primary' @click='createPost'>发布帖子</a-button>"
        >
          <a-list
            :data-source="posts"
            :loading="loading"
            :pagination="{ pageSize: 10 }"
          >
            <template #renderItem="{ item }">
              <a-list-item
                class="post-item"
                @click="goToPost(item.id)"
              >
                <a-list-item-meta
                  :title="item.title"
                  :description="`${item.username} · ${item.created_at}`"
                >
                  <template #avatar>
                    <a-avatar :src="item.avatar" />
                  </template>
                </a-list-item-meta>
                
                <div class="post-stats">
                  <a-space>
                    <span><EyeOutlined /> {{ item.view_count }}</span>
                    <span><LikeOutlined /> {{ item.like_count }}</span>
                    <span><MessageOutlined /> {{ item.comment_count }}</span>
                  </a-space>
                  
                  <a-tag v-if="item.is_top" color="red">置顶</a-tag>
                  <a-tag v-if="item.is_essence" color="gold">精华</a-tag>
                </div>
              </a-list-item>
            </template>
            
            <a-empty v-if="!loading && posts.length === 0" description="暂无帖子" />
          </a-list>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<style scoped>
.forum-view {
  max-width: 1200px;
  margin: 0 auto;
}

.post-item {
  cursor: pointer;
  transition: background-color 0.3s;
}

.post-item:hover {
  background-color: #f5f5f5;
}

.post-stats {
  display: flex;
  align-items: center;
  gap: 16px;
  color: #999;
  font-size: 14px;
}
</style>
