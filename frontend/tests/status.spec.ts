import { mount } from '@vue/test-utils'
import ElementPlus from 'element-plus'
import { describe, expect, it } from 'vitest'

import StatusTag from '../src/components/StatusTag.vue'
import { getStatusLabel, getStatusTagType } from '../src/utils/status'

describe('status display', () => {
  it.each([
    ['enabled', '启用', 'success'],
    ['1', '启用', 'success'],
    [1, '启用', 'success'],
    ['disabled', '停用', 'info'],
    ['0', '停用', 'info'],
    [0, '停用', 'info']
  ])('maps %s to %s', (value, label, type) => {
    expect(getStatusLabel(value)).toBe(label)
    expect(getStatusTagType(value)).toBe(type)
  })

  it('renders backend enabled values as enabled text', () => {
    const wrapper = mount(StatusTag, {
      props: {
        value: 'enabled'
      },
      global: {
        plugins: [ElementPlus]
      }
    })

    expect(wrapper.text()).toContain('启用')
  })
})
