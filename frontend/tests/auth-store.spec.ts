import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it } from 'vitest'
import { useAuthStore } from '../src/stores/auth'

describe('auth store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
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
})
