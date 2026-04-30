import { apiClient } from './client'

interface ApiResponse<T> {
  data: T
}

export interface PageParams {
  page: number
  page_size: number
  keyword?: string
}

export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export interface UserRow {
  id: number
  username: string
  nickname: string
  email?: string | null
  mobile?: string | null
  dept_id?: number | null
  status: string | number
  last_login_at?: string | null
}

export interface RoleRow {
  id: number
  code: string
  name: string
  data_scope: string
  sort: number
  status: string | number
}

export interface MenuRow {
  id: number
  parent_id?: number | null
  type: string
  title: string
  path?: string | null
  component?: string | null
  permission?: string | null
  icon?: string | null
  sort: number
  status: string | number
}

export interface DeptRow {
  id: number
  parent_id?: number | null
  ancestors: string
  name: string
  sort: number
  status: string | number
}

export interface PostRow {
  id: number
  code: string
  name: string
  sort: number
  status: string | number
}

export interface DictTypeRow {
  id: number
  code: string
  name: string
  status: string | number
}

export interface ConfigRow {
  id: number
  key: string
  name: string
  remark?: string | null
}

export interface LoginLogRow {
  id: number
  username: string
  success: boolean
  message?: string | null
  ip_address?: string | null
  user_agent?: string | null
  created_at: string
}

export interface OperationLogRow {
  id: number
  username?: string | null
  permission?: string | null
  title: string
  method?: string | null
  path?: string | null
  ip_address?: string | null
  success: boolean
  message?: string | null
  created_at: string
}

function listPage<T>(url: string, params: PageParams): Promise<PageResult<T>> {
  return apiClient.get<ApiResponse<PageResult<T>>>(url, { params }).then(response => response.data.data)
}

export function listUsers(params: PageParams) {
  return listPage<UserRow>('/system/users', params)
}

export function listRoles(params: PageParams) {
  return listPage<RoleRow>('/system/roles', params)
}

export function listMenus(params: PageParams) {
  return listPage<MenuRow>('/system/menus', params)
}

export function listDepts(params: PageParams) {
  return listPage<DeptRow>('/system/depts', params)
}

export function listPosts(params: PageParams) {
  return listPage<PostRow>('/system/posts', params)
}

export function listDictTypes(params: PageParams) {
  return listPage<DictTypeRow>('/system/dict-types', params)
}

export function listConfigs(params: PageParams) {
  return listPage<ConfigRow>('/system/configs', params)
}

export function listLoginLogs(params: PageParams) {
  return listPage<LoginLogRow>('/system/login-logs', params)
}

export function listOperationLogs(params: PageParams) {
  return listPage<OperationLogRow>('/system/operation-logs', params)
}
