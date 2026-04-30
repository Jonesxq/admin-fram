import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { loginApi, meApi } from '@/api/auth'
import { useAuthStore } from '../src/stores/auth'
import { useTabsStore } from '../src/stores/tabs'

vi.mock('@/api/auth', () => ({
  loginApi: vi.fn(),
  meApi: vi.fn()
}))

describe('auth store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.clearAllMocks()
  })

  it('stores token', () => {
    const store = useAuthStore()
    store.setToken('abc')
    expect(store.token).toBe('abc')
    expect(localStorage.getItem('access_token')).toBe('abc')
  })

  it('detects permission codes', () => {
    const store = useAuthStore()
    store.permissions = ['system:user:list']
    expect(store.hasPermission('system:user:list')).toBe(true)
    expect(store.hasPermission('system:user:delete')).toBe(false)
  })

  it('clears token when loading current user after login fails', async () => {
    vi.mocked(loginApi).mockResolvedValue({ access_token: 'abc', token_type: 'bearer' })
    vi.mocked(meApi).mockRejectedValue(new Error('profile failed'))

    const store = useAuthStore()

    await expect(store.login({ username: 'admin', password: 'secret' })).rejects.toThrow('profile failed')
    expect(store.token).toBe('')
    expect(localStorage.getItem('access_token')).toBeNull()
  })

  it('clears visited tabs on logout', () => {
    const authStore = useAuthStore()
    const tabsStore = useTabsStore()

    tabsStore.visitedTabs = [
      {
        path: '/dashboard',
        fullPath: '/dashboard',
        title: '仪表盘',
        affix: true
      },
      {
        path: '/system/users',
        fullPath: '/system/users',
        title: '用户管理',
        affix: false
      }
    ]

    authStore.logout()

    expect(tabsStore.visitedTabs).toEqual([])
  })
})
