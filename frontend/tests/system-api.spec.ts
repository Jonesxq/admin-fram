import { beforeEach, describe, expect, it, vi } from 'vitest'

import { apiClient } from '../src/api/client'
import {
  createConfig,
  createDept,
  createDictType,
  createMenu,
  createPost,
  createRole,
  createUser,
  deleteConfig,
  deleteDept,
  deleteDictType,
  deleteMenu,
  deletePost,
  deleteRole,
  deleteUser,
  listConfigs,
  listDepts,
  listDictTypes,
  listLoginLogs,
  listMenus,
  listOperationLogs,
  listPosts,
  listRoles,
  listUsers,
  updateConfig,
  updateDept,
  updateDictType,
  updateMenu,
  updatePost,
  updateRole,
  updateUser
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

  it.each([
    [createUser, '/system/users', { username: 'demo', password: 'Demo123!', nickname: 'Demo' }],
    [createRole, '/system/roles', { code: 'demo', name: 'Demo' }],
    [createMenu, '/system/menus', { type: 'menu', title: 'Demo' }],
    [createDept, '/system/depts', { name: 'Demo' }],
    [createPost, '/system/posts', { code: 'demo', name: 'Demo' }],
    [createDictType, '/system/dict-types', { code: 'demo', name: 'Demo' }],
    [createConfig, '/system/configs', { key: 'demo.key', value: 'demo', name: 'Demo' }]
  ])('creates resource through %s', async (creator, endpoint, payload) => {
    const created = { id: 1, ...payload }
    const post = vi.spyOn(apiClient, 'post').mockResolvedValue({ data: { data: created } })

    await expect(creator(payload as never)).resolves.toBe(created)
    expect(post).toHaveBeenCalledWith(endpoint, payload)
  })

  it.each([
    [updateUser, '/system/users/8', { nickname: 'Demo' }],
    [updateRole, '/system/roles/8', { name: 'Demo' }],
    [updateMenu, '/system/menus/8', { title: 'Demo' }],
    [updateDept, '/system/depts/8', { name: 'Demo' }],
    [updatePost, '/system/posts/8', { name: 'Demo' }],
    [updateDictType, '/system/dict-types/8', { name: 'Demo' }],
    [updateConfig, '/system/configs/8', { name: 'Demo' }]
  ])('updates resource through %s', async (updater, endpoint, payload) => {
    const updated = { id: 8, ...payload }
    const put = vi.spyOn(apiClient, 'put').mockResolvedValue({ data: { data: updated } })

    await expect(updater(8, payload as never)).resolves.toBe(updated)
    expect(put).toHaveBeenCalledWith(endpoint, payload)
  })

  it.each([
    [deleteUser, '/system/users/8'],
    [deleteRole, '/system/roles/8'],
    [deleteMenu, '/system/menus/8'],
    [deleteDept, '/system/depts/8'],
    [deletePost, '/system/posts/8'],
    [deleteDictType, '/system/dict-types/8'],
    [deleteConfig, '/system/configs/8']
  ])('deletes resource through %s', async (remover, endpoint) => {
    const deleted = { id: 8 }
    const remove = vi.spyOn(apiClient, 'delete').mockResolvedValue({ data: { data: deleted } })

    await expect(remover(8)).resolves.toBe(deleted)
    expect(remove).toHaveBeenCalledWith(endpoint)
  })
})
