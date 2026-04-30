import { beforeEach, describe, expect, it, vi } from 'vitest'

import { apiClient } from '../src/api/client'
import {
  listConfigs,
  listDepts,
  listDictTypes,
  listLoginLogs,
  listMenus,
  listOperationLogs,
  listPosts,
  listRoles,
  listUsers
} from '../src/api/system'

describe('system api', () => {
  const pageParams = { page: 2, page_size: 20, keyword: 'admin' }

  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it.each([
    [listUsers, '/system/users'],
    [listRoles, '/system/roles'],
    [listMenus, '/system/menus'],
    [listDepts, '/system/depts'],
    [listPosts, '/system/posts'],
    [listDictTypes, '/system/dict-types'],
    [listConfigs, '/system/configs'],
    [listLoginLogs, '/system/login-logs'],
    [listOperationLogs, '/system/operation-logs']
  ])('loads list data from %s with unified pagination params', async (loader, endpoint) => {
    const result = { items: [], total: 0, page: 2, page_size: 20 }
    const get = vi.spyOn(apiClient, 'get').mockResolvedValue({ data: { data: result } })

    await expect(loader(pageParams)).resolves.toBe(result)
    expect(get).toHaveBeenCalledWith(endpoint, { params: pageParams })
  })
})
