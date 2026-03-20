import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    loading: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.user,
  },

  actions: {
    async fetchCSRF() {
      await api.get('/auth/csrf/')
    },

    async login(username, password) {
      await this.fetchCSRF()
      const { data } = await api.post('/auth/login/', { username, password })
      this.user = data
      return data
    },

    async logout() {
      await api.post('/auth/logout/')
      this.user = null
    },

    async checkAuth() {
      try {
        const { data } = await api.get('/auth/me/')
        this.user = data
      } catch {
        this.user = null
      }
    },
  },
})
