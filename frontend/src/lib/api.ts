import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to all requests
api.interceptors.request.use((config) => {
  const state = useAuthStore.getState()
  if (state.session?.access_token) {
    config.headers.Authorization = `Bearer ${state.session.access_token}`
  }
  return config
})

// Notification preferences API
export const notificationApi = {
  getPreferences: () => api.get('/notifications/preferences'),
  updatePreferences: (prefs: {
    action_plan_reminders: boolean
    weekly_summary: boolean
    marketing: boolean
  }) => api.put('/notifications/preferences', prefs),
  sendTestEmail: (email: string) => api.post('/notifications/test', { email }),
  sendNotification: (type: string, data?: object) =>
    api.post('/notifications/send', { type, data }),
}

export default api