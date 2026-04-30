import { describe, expect, it } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'

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

  it('admin role grants every permission', () => {
    setActivePinia(createPinia())

    const store = useAuthStore()

    store.roles = ['admin']

    expect(store.hasPermission('system:anything')).toBe(true)
  })
})
