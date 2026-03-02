<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

const packages = ref([])
const categories = ref([])
const loading = ref(false)
const searchQuery = ref('')
const selectedCategory = ref(route.query.category || null)
const sortBy = ref('-created_at')

const priceRange = ref([0, 10000])
const hasCostume = ref(null)

const fetchCategories = async () => {
  try {
    const response = await axios.get('/api/packages/categories/')
    categories.value = response.data.results || response.data
  } catch (err) {
    console.error('获取分类失败', err)
  }
}

const fetchPackages = async () => {
  loading.value = true
  try {
    const params: any = {
      ordering: sortBy.value,
    }
    
    if (selectedCategory.value) {
      params.category = selectedCategory.value
    }
    
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    
    if (hasCostume.value !== null) {
      params.has_costume = hasCostume.value
    }
    
    const response = await axios.get('/api/packages/packages/', { params })
    packages.value = response.data.results || []
  } catch (err) {
    console.error('获取套餐失败', err)
  } finally {
    loading.value = false
  }
}

const selectCategory = (categoryId) => {
  selectedCategory.value = categoryId
  router.push({ query: { ...route.query, category: categoryId } })
  fetchPackages()
}

const goToPackage = (id) => {
  router.push(`/package/${id}`)
}

const handleSearch = () => {
  fetchPackages()
}

const handleSortChange = (value) => {
  sortBy.value = value
  fetchPackages()
}

watch(() => route.query.category, (newVal) => {
  selectedCategory.value = newVal
  fetchPackages()
})

onMounted(() => {
  fetchCategories()
  fetchPackages()
})
</script>

<template>
  <div class="packages-view">
    <a-row :gutter="24">
      <!-- 左侧筛选 -->
      <a-col :span="5">
        <a-card title="筛选条件">
          <a-menu
            mode="inline"
            :selectedKeys="[selectedCategory]"
            @click="({ key }) => selectCategory(key)"
          >
            <a-menu-item :key="null">全部套餐</a-menu-item>
            <a-menu-item v-for="cat in categories" :key="cat.id">
              {{ cat.name }}
            </a-menu-item>
          </a-menu>
          
          <a-divider />
          
          <div class="filter-section">
            <h4>服装妆造</h4>
            <a-radio-group v-model:value="hasCostume" @change="fetchPackages">
              <a-radio :value="null">全部</a-radio>
              <a-radio :value="true">包含</a-radio>
              <a-radio :value="false">不包含</a-radio>
            </a-radio-group>
          </div>
        </a-card>
      </a-col>
      
      <!-- 右侧列表 -->
      <a-col :span="19">
        <a-card
          :title="`摄影套餐 (${packages.length})`"
          :loading="loading"
        >
          <template #extra>
            <a-space>
              <a-input-search
                v-model:value="searchQuery"
                placeholder="搜索套餐"
                style="width: 200px"
                @search="handleSearch"
              />
              
              <a-select
                v-model:value="sortBy"
                style="width: 120px"
                @change="handleSortChange"
              >
                <a-select-option value="-created_at">最新发布</a-select-option>
                <a-select-option value="-booking_count">最受欢迎</a-select-option>
                <a-select-option value="current_price">价格从低到高</a-select-option>
                <a-select-option value="-current_price">价格从高到低</a-select-option>
              </a-select>
            </a-space>
          </template>
          
          <a-row :gutter="[16, 16]">
            <a-col
              v-for="pkg in packages"
              :key="pkg.id"
              :xs="24"
              :sm="12"
              :md="8"
              :lg="6"
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
                
                <a-typography-title :level="5" class="package-title">
                  {{ pkg.name }}
                </a-typography-title>
                
                <a-space class="package-tags">
                  <a-tag v-for="tag in pkg.tags?.slice(0, 2)" :key="tag">
                    {{ tag }}
                  </a-tag>
                </a-space>
                
                <div class="package-features">
                  <span>底片{{ pkg.base_photo_count }}张</span>
                  <span>精修{{ pkg.retouch_count }}张</span>
                  <a-tag v-if="pkg.has_costume" size="small">含服装</a-tag>
                </div>
                
                <div class="package-footer">
                  <div class="price-section">
                    <span class="current-price">¥{{ pkg.current_price }}</span>
                    <span v-if="pkg.original_price > pkg.current_price" class="original-price">
                      ¥{{ pkg.original_price }}
                    </span>
                  </div>
                  
                  <span class="booking-count">{{ pkg.booking_count }}人已预约</span>
                </div>
              </a-card>
            </a-col>
          </a-row>
          
          <a-empty v-if="!loading && packages.length === 0" description="暂无套餐" />
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<style scoped>
.packages-view {
  max-width: 1400px;
  margin: 0 auto;
}

.filter-section {
  padding: 0 16px;
}

.filter-section h4 {
  margin-bottom: 12px;
  font-weight: 500;
}

.package-card {
  cursor: pointer;
  transition: all 0.3s;
}

.package-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.package-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 4px;
}

.package-title {
  margin: 12px 0 8px;
  font-size: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.package-tags {
  margin-bottom: 8px;
}

.package-features {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 12px;
  color: #666;
}

.package-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.current-price {
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
  color: #999;
  font-size: 12px;
}
</style>
