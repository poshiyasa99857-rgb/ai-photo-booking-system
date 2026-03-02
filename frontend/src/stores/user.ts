import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')
  const loading = ref(false)
  const error = ref('')

  // Getters
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.is_admin || false)

  // Actions
  const login = async (credentials: { username: string; password: string }) => {
    loading.value = true
    error.value = ''
    
    try {
      const response = await axios.post(`${API_BASE_URL}/users/login/`, credentials)
      user.value = response.data.user
      // Django使用session，这里简化处理
      return true
    } catch (err: any) {
      error.value = err.response?.data?.error || '登录失败'
      return false
    } finally {
      loading.value = false
    }
  }

  const register = async (data: {
    username: string
    email: string
    phone: string
    password: string
    confirm_password: string
  }) => {
    loading.value = true
    error.value = ''
    
    try {
      const response = await axios.post(`${API_BASE_URL}/users/register/`, data)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.error || '注册失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      await axios.post(`${API_BASE_URL}/users/logout/`)
    } finally {
      user.value = null
      token.value = ''
      localStorage.removeItem('token')
    }
  }

  const fetchProfile = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/users/me/`)
      user.value = response.data
    } catch (err) {
      console.error('获取用户信息失败', err)
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isLoggedIn,
    isAdmin,
    login,
    register,
    logout,
    fetchProfile,
  }
}, {
  persist: true,
})
