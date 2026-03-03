<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { message } from 'ant-design-vue'

const tasks = ref([])
const logs = ref([])
const loading = ref(false)
const logLoading = ref(false)
const modalVisible = ref(false)
const editingTask = ref(null)

const taskForm = ref({
  name: '',
  task_type: 'backup',
  cron_expression: '0 0 * * *',
  params: {},
  is_active: true,
})

const taskTypes = [
  { value: 'backup', label: '数据备份', desc: '自动备份数据库' },
  { value: 'cleanup', label: '数据清理', desc: '清理过期日志和数据' },
  { value: 'report', label: '生成报表', desc: '生成每日统计报表' },
  { value: 'notification', label: '发送通知', desc: '发送预约提醒等' },
  { value: 'ai_sync', label: 'AI数据同步', desc: '同步AI使用数据' },
  { value: 'custom', label: '自定义任务', desc: '执行自定义脚本' },
]

const fetchTasks = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/analytics/tasks/')
    tasks.value = response.data.results || []
  } catch (err) {
    message.error('获取任务列表失败')
  } finally {
    loading.value = false
  }
}

const fetchLogs = async () => {
  logLoading.value = true
  try {
    const response = await axios.get('/api/analytics/task-logs/')
    logs.value = response.data.results || []
  } catch (err) {
    console.error('获取日志失败', err)
  } finally {
    logLoading.value = false
  }
}

const showCreateModal = () => {
  editingTask.value = null
  taskForm.value = {
    name: '',
    task_type: 'backup',
    cron_expression: '0 0 * * *',
    params: {},
    is_active: true,
  }
  modalVisible.value = true
}

const saveTask = async () => {
  try {
    if (editingTask.value) {
      await axios.put(`/api/analytics/tasks/${editingTask.value.id}/`, taskForm.value)
      message.success('更新成功')
    } else {
      await axios.post('/api/analytics/tasks/', taskForm.value)
      message.success('创建成功')
    }
    modalVisible.value = false
    fetchTasks()
  } catch (err) {
    message.error('保存失败')
  }
}

const runTaskNow = async (id) => {
  try {
    await axios.post(`/api/analytics/tasks/${id}/run_now/`)
    message.success('任务执行成功')
    fetchLogs()
  } catch (err) {
    message.error('执行失败')
  }
}

onMounted(() => {
  fetchTasks()
  fetchLogs()
})
</script>

<template>
  <div class="task-management-view">
    <a-card title="定时任务管理" :loading="loading">
      <template #extra>
        <a-button type="primary" @click="showCreateModal">新建任务</a-button>
      </template>
      
      <a-list :data-source="tasks">
        <template #renderItem="{ item }">
          <a-list-item>
            <a-list-item-meta
              :title="item.name"
              :description="`类型: ${item.task_type} | Cron: ${item.cron_expression}`"
            />
            
            <a-space>
              <a-switch :checked="item.is_active" />
              <a-button type="link" @click="() => runTaskNow(item.id)">立即执行</a-button>
            </a-space>
          </a-list-item>
        </template>
      </a-list>
    </a-card>
    
    <a-modal v-model:visible="modalVisible" title="定时任务">
      <a-form :model="taskForm" layout="vertical">
        <a-form-item label="任务名称">
          <a-input v-model:value="taskForm.name" />
        </a-form-item>
        
        <a-form-item label="任务类型">
          <a-select v-model:value="taskForm.task_type">
            <a-select-option v-for="t in taskTypes" :key="t.value" :value="t.value"
              {{ t.label }}
            </a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item label="Cron表达式">
          <a-input v-model:value="taskForm.cron_expression" />
        </a-form-item>
        
        <a-form-item>
          <a-button type="primary" @click="saveTask">保存</a-button>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<style scoped>
.task-management-view {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
