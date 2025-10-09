import axios from 'axios'
import toast from 'react-hot-toast'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://ai-agent-ikc8.onrender.com'

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    
    const message = error.response?.data?.detail || error.message || 'An error occurred'
    toast.error(message)
    
    return Promise.reject(error)
  }
)

// API endpoints
export const authAPI = {
  login: (username, password) => api.get(`/auth/login?username=${username}&password=${password}`)
}

export const contentAPI = {
  upload: (formData) => api.post('/content/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  list: () => api.get('/content/sources'),
  getById: (id) => api.get(`/content/sources/${id}`)
}

export const generationAPI = {
  generate: (data) => api.post('/ai/generate', data),
  demoGenerate: (data) => api.post('/demo/generate', data),
  getStatus: () => api.get('/ai/status')
}

export const adminAPI = {
  dbStatus: () => api.get('/admin/db-status'),
  initDb: () => api.post('/admin/init-db')
}
