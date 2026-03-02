<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { message } from 'ant-design-vue'

const router = useRouter()

const categories = ref([])
const hotPackages = ref([])
const loading = ref(false)

const fetchCategories = async () => {
  try {
    const response = await axios.get('/api/packages/categories/')
    categories.value = response.data.results || response.data
  } catch (err) {
    console.error('获取分类失败', err)
  }
}

const fetchHotPackages = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/packages/packages/?ordering=-booking_count&page_size=6')
    hotPackages.value = response.data.results || []
  } catch (err) {
    console.error('获取热门套餐失败', err)
  } finally {
    loading.value = false
  }
}

const goToCategory = (categoryId: number) => {
  router.push(`/packages?category=${categoryId}`)
}

const goToPackage = (packageId: number) => {
  router.push(`/package/${packageId}`)
}

onMounted(() => {
  fetchCategories()
  fetchHotPackages()
})
</script>

<template>
  <div class="home-view">
    <!-- Hero Section -->
    <div class="hero-section">
      <a-typography-title :level="1" style="color: white; margin-bottom: 16px">
        发现美好瞬间
      </a-typography-title>
      <a-typography-paragraph style="color: rgba(255,255,255,0.85); font-size: 18px">
        AI智能推荐，为您匹配最适合的摄影套餐
      </a-typography-paragraph>
      
      <a-space size="large" style="margin-top: 24px">
        <a-button type="primary" size="large" @click="$router.push('/packages')">
          浏览套餐
        </a-button>
        <a-button size="large" @click="$router.push('/ai-chat')">
          咨询AI助手
        </a-button>
      </a-space>
    </div>
    
    <!-- Categories Section -->
    <a-card title="服务分类" class="section-card">
      <a-row :gutter="[16, 16]">
        <a-col
          v-for="category in categories"
          :key="category.id"
          :xs="12"
          :sm="8"
          :md="6"
          :lg="4"
        >
          <a-card
            hoverable
            class="category-card"
            @click="goToCategory(category.id)"
          >
            <a-typography-title :level="4" style="margin: 0">
              {{ category.name }}
            </a-typography-title>
            <a-typography-text type="secondary">
              {{ category.description }}
            </a-typography-text>
          </a-card>
        </a-col>
      </a-row>
    </a-card>
    
    <!-- Hot Packages Section -->
    <a-card title="热门套餐" class="section-card" :loading="loading">
      <a-row :gutter="[16, 16]">
        <a-col
          v-for="pkg in hotPackages"
          :key="pkg.id"
          :xs="24"
          :sm="12"
          :md="8"
        >
          <a-card
            hoverable
            class="package-card"
            @click="goToPackage(pkg.id)"
          >
            <img
              :src="pkg.cover_image || '/placeholder.jpg'"
              class="package-image"
              :alt="pkg.name"
            />
            <a-typography-title :level="5" style="margin: 12px 0 8px">
              {{ pkg.name }}
            </a-typography-title>
            
            <a-space style="margin-bottom: 8px">
              <a-tag v-for="tag in pkg.tags.slice(0, 3)" :key="tag">{{ tag }}</a-tag>
            </a-space>
            
            <div class="package-meta">
              <span class="price">¥{{ pkg.current_price }}</span>
              <span v-if="pkg.original_price > pkg.current_price" class="original-price">
                ¥{{ pkg.original_price }}
              </span>
              <span class="booking-count">{{ pkg.booking_count }}人已预约</span>
            </div>
          </a-card>
        </a-col>
      </a-row>
      
      <a-empty v-if="!loading && hotPackages.length === 0" description="暂无数据" />
    </a-card>
  </div>
</template>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 80px 24px;
  text-align: center;
  border-radius: 8px;
  margin-bottom: 24px;
}

.section-card {
  margin-bottom: 24px;
}

.category-card {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.category-card:hover {
  transform: translateY(-4px);
}

.package-card {
  cursor: pointer;
}

.package-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
}

.package-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}

.price {
  color: #f5222d;
  font-size: 20px;
  font-weight: bold;
}

.original-price {
  color: #999;
  text-decoration: line-through;
  font-size: 14px;
}

.booking-count {
  color: #666;
  font-size: 12px;
  margin-left: auto;
}
</style>
