import { defineStore } from 'pinia'

import { loginApi, meApi, type AuthMenu, type AuthUser, type LoginPayload } from '@/api/auth'

interface AuthState {
  token: string
  user: AuthUser | null
  roles: string[]
  permissions: string[]
  menus: AuthMenu[]
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('access_token') ?? '',
    user: null,
    roles: [],
    permissions: [],
    menus: []
  }),
  actions: {
    setToken(token: string) {
      this.token = token

      if (token) {
        localStorage.setItem('access_token', token)
      } else {
        localStorage.removeItem('access_token')
      }
    },
    async login(payload: LoginPayload) {
      const result = await loginApi(payload)

      this.setToken(result.access_token)

      try {
        await this.fetchMe()
      } catch (error) {
        this.logout()
        throw error
      }

      return result
    },
    async fetchMe() {
      const result = await meApi()

      this.user = result.user
      this.roles = result.roles
      this.permissions = result.permissions
      this.menus = result.menus

      return result
    },
    logout() {
      this.setToken('')
      this.user = null
      this.roles = []
      this.permissions = []
      this.menus = []
    },
    hasPermission(permission: string) {
      if (this.roles.includes('admin')) {
        return true
      }

      return this.permissions.includes(permission)
    }
  }
})
