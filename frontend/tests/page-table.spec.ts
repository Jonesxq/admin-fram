import { flushPromises, mount } from '@vue/test-utils'
import ElementPlus from 'element-plus'
import { describe, expect, it, vi } from 'vitest'
import { nextTick } from 'vue'

import PageTable from '../src/components/PageTable.vue'
import type { PageResult } from '../src/api/system'

function deferred<T>() {
  let resolve!: (value: T) => void
  const promise = new Promise<T>(innerResolve => {
    resolve = innerResolve
  })

  return { promise, resolve }
}

describe('PageTable', () => {
  it('keeps the latest request result when an older request resolves later', async () => {
    const first = deferred<PageResult<unknown>>()
    const second = deferred<PageResult<unknown>>()
    const loader = vi.fn().mockReturnValueOnce(first.promise).mockReturnValueOnce(second.promise)

    const wrapper = mount(PageTable, {
      props: {
        columns: [{ prop: 'name', label: '名称' }],
        loader,
        rowKey: 'id'
      },
      global: {
        plugins: [ElementPlus]
      }
    })

    await nextTick()
    await wrapper.findAll('button').find(button => button.text() === '刷新')?.trigger('click')
    second.resolve({ items: [{ id: 2, name: '新数据' }], total: 1, page: 1, page_size: 10 })
    await flushPromises()
    await nextTick()

    expect(wrapper.text()).toContain('新数据')

    first.resolve({ items: [{ id: 1, name: '旧数据' }], total: 1, page: 1, page_size: 10 })
    await flushPromises()
    await nextTick()

    expect(wrapper.text()).toContain('新数据')
    expect(wrapper.text()).not.toContain('旧数据')
  })

  it('hides keyword search by default while keeping refresh and table rendering', async () => {
    const loader = vi.fn().mockResolvedValue({
      items: [{ id: 1, name: '用户A' }],
      total: 1,
      page: 1,
      page_size: 10
    })

    const wrapper = mount(PageTable, {
      props: {
        columns: [{ prop: 'name', label: '名称' }],
        loader,
        rowKey: 'id'
      },
      global: {
        plugins: [ElementPlus]
      }
    })

    await flushPromises()

    expect(wrapper.find('.page-table__search').exists()).toBe(false)
    expect(wrapper.text()).not.toContain('查询')
    expect(wrapper.text()).toContain('刷新')
    expect(wrapper.text()).toContain('用户A')
  })

  it('submits keyword to loader only when search is explicitly enabled', async () => {
    const loader = vi.fn().mockResolvedValue({
      items: [],
      total: 0,
      page: 1,
      page_size: 10
    })

    const wrapper = mount(PageTable, {
      props: {
        columns: [{ prop: 'name', label: '名称' }],
        loader,
        rowKey: 'id',
        searchable: true
      },
      global: {
        plugins: [ElementPlus]
      }
    })

    await flushPromises()
    await wrapper.find('.page-table__search input').setValue('admin')
    await wrapper.findAll('button').find(button => button.text() === '查询')?.trigger('click')
    await flushPromises()

    expect(wrapper.find('.page-table__search').exists()).toBe(true)
    expect(loader).toHaveBeenLastCalledWith({
      page: 1,
      page_size: 10,
      keyword: 'admin'
    })
  })
})
