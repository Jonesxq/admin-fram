import { flushPromises, mount } from '@vue/test-utils'
import ElementPlus from 'element-plus'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import LoginView from '../src/views/login/LoginView.vue'

const login = vi.fn()
const replace = vi.fn()
let query: Record<string, string | undefined> = {}

vi.mock('@/stores/auth', () => ({
  useAuthStore: () => ({ login })
}))

vi.mock('vue-router', () => ({
  useRoute: () => ({ query }),
  useRouter: () => ({ replace })
}))

describe('LoginView', () => {
  beforeEach(() => {
    login.mockReset()
    replace.mockReset()
    query = {}
  })

  it('logs in and redirects to query redirect when credentials are valid', async () => {
    login.mockResolvedValue({ access_token: 'token', token_type: 'bearer' })
    query = { redirect: '/system/users' }

    const wrapper = mount(LoginView, {
      global: {
        plugins: [ElementPlus]
      }
    })

    await wrapper.find('[data-testid="login-username"] input').setValue('admin')
    await wrapper.find('[data-testid="login-password"] input').setValue('Admin123!')
    await wrapper.find('[data-testid="login-submit"]').trigger('click')
    await flushPromises()

    expect(login).toHaveBeenCalledWith({ username: 'admin', password: 'Admin123!' })
    expect(replace).toHaveBeenCalledWith('/system/users')
  })

  it('logs in and redirects to dashboard when no redirect is provided', async () => {
    login.mockResolvedValue({ access_token: 'token', token_type: 'bearer' })

    const wrapper = mount(LoginView, {
      global: {
        plugins: [ElementPlus]
      }
    })

    await wrapper.find('[data-testid="login-username"] input').setValue('admin')
    await wrapper.find('[data-testid="login-password"] input').setValue('Admin123!')
    await wrapper.find('[data-testid="login-submit"]').trigger('click')
    await flushPromises()

    expect(replace).toHaveBeenCalledWith('/dashboard')
  })
})
