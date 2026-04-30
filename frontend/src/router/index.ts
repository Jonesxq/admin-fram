import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

import { staticRoutes } from './static-routes'

export const router = createRouter({
  history: createWebHistory(),
  routes: staticRoutes
})

router.beforeEach(async to => {
  if (to.path === '/login') {
    return true
  }

  const authStore = useAuthStore()

  if (!authStore.token) {
    return {
      path: '/login',
      query: {
        redirect: to.fullPath
      }
    }
  }

  if (!authStore.user) {
    try {
      await authStore.fetchMe()
    } catch {
      authStore.logout()

      return {
        path: '/login',
        query: {
          redirect: to.fullPath
        }
      }
    }
  }

  return true
})
