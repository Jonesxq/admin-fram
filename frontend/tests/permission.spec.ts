import { describe, expect, it } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'

import { staticRoutes } from '../src/router/static-routes'
import { useAuthStore } from '../src/stores/auth'

describe('static routes', () => {
  it('contains login outside layout and dashboard inside admin layout', () => {
    expect(staticRoutes.some(route => route.path === '/login')).toBe(true)

    const adminLayout = staticRoutes.find(route =>
      route.children?.some(child => child.path === '/dashboard')
    )

    expect(adminLayout).toBeTruthy()
    expect(adminLayout?.children?.some(route => route.path === '/dashboard')).toBe(true)
  })

  it('mounts system and example pages as real admin layout routes', () => {
    const adminLayout = staticRoutes.find(route =>
      route.children?.some(child => child.path === '/dashboard')
    )
    const childPaths = adminLayout?.children?.map(route => route.path) ?? []

    expect(childPaths).toEqual(
      expect.arrayContaining([
        '/system',
        '/system/users',
        '/system/roles',
        '/system/menus',
        '/system/depts',
        '/system/posts',
        '/system/dicts',
        '/system/configs',
        '/system/login-logs',
        '/system/operation-logs',
        '/monitor/login-logs',
        '/monitor/operation-logs',
        '/examples',
        '/examples/list',
        '/examples/form',
        '/examples/detail'
      ])
    )
    expect(childPaths).not.toContain('/system/:pathMatch(.*)*')
    expect(childPaths).not.toContain('/examples/:pathMatch(.*)*')
  })

  it('resolves legacy monitor log menu paths without falling through to 404', async () => {
    const router = createRouter({
      history: createWebHistory(),
      routes: staticRoutes
    })

    const loginLogMatches = router.resolve('/monitor/login-logs').matched
    const operationLogMatches = router.resolve('/monitor/operation-logs').matched

    expect(loginLogMatches[loginLogMatches.length - 1]?.name).not.toBe('NotFound')
    expect(operationLogMatches[operationLogMatches.length - 1]?.name).not.toBe('NotFound')
  })

  it('admin role grants every permission', () => {
    setActivePinia(createPinia())

    const store = useAuthStore()

    store.roles = ['admin']

    expect(store.hasPermission('system:anything')).toBe(true)
  })
})
