import { mount } from '@vue/test-utils'
import ElementPlus, { ElMessage } from 'element-plus'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import TopBar from '../src/layouts/components/TopBar.vue'

vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn()
  })
}))

describe('TopBar', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.restoreAllMocks()
  })

  it('handles fullscreen request rejection without throwing', async () => {
    const requestFullscreen = vi.fn().mockRejectedValue(new Error('fullscreen failed'))
    const messageWarning = vi.spyOn(ElMessage, 'warning').mockImplementation(() => undefined as never)

    Object.defineProperty(document, 'fullscreenEnabled', {
      configurable: true,
      value: true
    })
    Object.defineProperty(document, 'fullscreenElement', {
      configurable: true,
      value: null
    })
    Object.defineProperty(document.documentElement, 'requestFullscreen', {
      configurable: true,
      value: requestFullscreen
    })

    const wrapper = mount(TopBar, {
      global: {
        plugins: [ElementPlus],
        stubs: {
          Teleport: true
        }
      }
    })

    await expect(wrapper.get('[aria-label="全屏"]').trigger('click')).resolves.toBeUndefined()
    expect(requestFullscreen).toHaveBeenCalledTimes(1)
    expect(messageWarning).toHaveBeenCalledWith('全屏切换失败')
  })
})
