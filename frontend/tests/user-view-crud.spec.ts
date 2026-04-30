import { flushPromises, mount } from '@vue/test-utils'
import ElementPlus from 'element-plus'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import UserView from '../src/views/system/UserView.vue'
import { createUser, listUsers } from '../src/api/system'

vi.mock('../src/api/system', () => ({
  createUser: vi.fn(),
  deleteUser: vi.fn(),
  listUsers: vi.fn(),
  updateUser: vi.fn()
}))

vi.mock('@/stores/auth', () => ({
  useAuthStore: () => ({
    hasPermission: () => true,
    roles: ['admin'],
    permissions: []
  })
}))

describe('UserView CRUD', () => {
  beforeEach(() => {
    vi.mocked(listUsers).mockReset()
    vi.mocked(createUser).mockReset()
    document.body.innerHTML = ''
  })

  it('creates a user from the dialog and refreshes the table', async () => {
    vi.mocked(listUsers).mockResolvedValue({
      items: [],
      total: 0,
      page: 1,
      page_size: 10
    })
    vi.mocked(createUser).mockResolvedValue({
      id: 3,
      username: 'demo',
      nickname: 'Demo',
      status: 'enabled'
    })

    const wrapper = mount(UserView, {
      attachTo: document.body,
      global: {
        plugins: [ElementPlus]
      }
    })

    await flushPromises()
    await wrapper.find('[data-testid="crud-create-button"]').trigger('click')
    await flushPromises()

    await wrapper.find('[data-testid="field-username"] input').setValue('demo')
    await wrapper.find('[data-testid="field-password"] input').setValue('Demo123!')
    await wrapper.find('[data-testid="field-nickname"] input').setValue('Demo')
    await wrapper.find('[data-testid="crud-submit"]').trigger('click')
    await flushPromises()

    expect(createUser).toHaveBeenCalledWith(
      expect.objectContaining({
        username: 'demo',
        password: 'Demo123!',
        nickname: 'Demo',
        status: 'enabled'
      })
    )
    expect(listUsers).toHaveBeenCalledTimes(2)
  })
})
