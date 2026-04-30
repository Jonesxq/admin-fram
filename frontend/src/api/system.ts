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

export interface UserCreatePayload {
  username: string
  password: string
  nickname: string
  email?: string | null
  mobile?: string | null
  dept_id?: number | null
  status?: string
}

export interface UserUpdatePayload {
  nickname?: string
  email?: string | null
  mobile?: string | null
  dept_id?: number | null
  status?: string
}

export interface RoleRow {
  id: number
  code: string
  name: string
  data_scope: string
  sort: number
  status: string | number
}

export interface RolePayload {
  code: string
  name: string
  data_scope?: string
  sort?: number
  status?: string
}

export type RoleUpdatePayload = Partial<RolePayload>

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

export interface MenuPayload {
  type: string
  title: string
  parent_id?: number | null
  path?: string | null
  component?: string | null
  permission?: string | null
  icon?: string | null
  sort?: number
  status?: string
}

export type MenuUpdatePayload = Partial<MenuPayload>

export interface DeptRow {
  id: number
  parent_id?: number | null
  ancestors: string
  name: string
  sort: number
  status: string | number
}

export interface DeptPayload {
  name: string
  parent_id?: number | null
  ancestors?: string
  sort?: number
  status?: string
}

export type DeptUpdatePayload = Partial<DeptPayload>

export interface PostRow {
  id: number
  code: string
  name: string
  sort: number
  status: string | number
}

export interface PostPayload {
  code: string
  name: string
  sort?: number
  status?: string
}

export type PostUpdatePayload = Partial<PostPayload>

export interface DictTypeRow {
  id: number
  code: string
  name: string
  status: string | number
}

export interface DictTypePayload {
  code: string
  name: string
  status?: string
}

export type DictTypeUpdatePayload = Partial<DictTypePayload>

export interface ConfigRow {
  id: number
  key: string
  name: string
  remark?: string | null
}

export interface ConfigCreatePayload {
  key: string
  value: string
  name: string
  remark?: string | null
}

export interface ConfigUpdatePayload {
  key?: string
  value?: string
  name?: string
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

function createResource<T, P>(url: string, payload: P): Promise<T> {
  return apiClient.post<ApiResponse<T>>(url, payload).then(response => response.data.data)
}

function updateResource<T, P>(url: string, payload: P): Promise<T> {
  return apiClient.put<ApiResponse<T>>(url, payload).then(response => response.data.data)
}

function deleteResource(url: string): Promise<{ id: number }> {
  return apiClient.delete<ApiResponse<{ id: number }>>(url).then(response => response.data.data)
}

export function listUsers(params: PageParams) {
  return listPage<UserRow>('/system/users', params)
}

export function createUser(payload: UserCreatePayload) {
  return createResource<UserRow, UserCreatePayload>('/system/users', payload)
}

export function updateUser(id: number, payload: UserUpdatePayload) {
  return updateResource<UserRow, UserUpdatePayload>(`/system/users/${id}`, payload)
}

export function deleteUser(id: number) {
  return deleteResource(`/system/users/${id}`)
}

export function listRoles(params: PageParams) {
  return listPage<RoleRow>('/system/roles', params)
}

export function createRole(payload: RolePayload) {
  return createResource<RoleRow, RolePayload>('/system/roles', payload)
}

export function updateRole(id: number, payload: RoleUpdatePayload) {
  return updateResource<RoleRow, RoleUpdatePayload>(`/system/roles/${id}`, payload)
}

export function deleteRole(id: number) {
  return deleteResource(`/system/roles/${id}`)
}

export function listMenus(params: PageParams) {
  return listPage<MenuRow>('/system/menus', params)
}

export function createMenu(payload: MenuPayload) {
  return createResource<MenuRow, MenuPayload>('/system/menus', payload)
}

export function updateMenu(id: number, payload: MenuUpdatePayload) {
  return updateResource<MenuRow, MenuUpdatePayload>(`/system/menus/${id}`, payload)
}

export function deleteMenu(id: number) {
  return deleteResource(`/system/menus/${id}`)
}

export function listDepts(params: PageParams) {
  return listPage<DeptRow>('/system/depts', params)
}

export function createDept(payload: DeptPayload) {
  return createResource<DeptRow, DeptPayload>('/system/depts', payload)
}

export function updateDept(id: number, payload: DeptUpdatePayload) {
  return updateResource<DeptRow, DeptUpdatePayload>(`/system/depts/${id}`, payload)
}

export function deleteDept(id: number) {
  return deleteResource(`/system/depts/${id}`)
}

export function listPosts(params: PageParams) {
  return listPage<PostRow>('/system/posts', params)
}

export function createPost(payload: PostPayload) {
  return createResource<PostRow, PostPayload>('/system/posts', payload)
}

export function updatePost(id: number, payload: PostUpdatePayload) {
  return updateResource<PostRow, PostUpdatePayload>(`/system/posts/${id}`, payload)
}

export function deletePost(id: number) {
  return deleteResource(`/system/posts/${id}`)
}

export function listDictTypes(params: PageParams) {
  return listPage<DictTypeRow>('/system/dict-types', params)
}

export function createDictType(payload: DictTypePayload) {
  return createResource<DictTypeRow, DictTypePayload>('/system/dict-types', payload)
}

export function updateDictType(id: number, payload: DictTypeUpdatePayload) {
  return updateResource<DictTypeRow, DictTypeUpdatePayload>(`/system/dict-types/${id}`, payload)
}

export function deleteDictType(id: number) {
  return deleteResource(`/system/dict-types/${id}`)
}

export function listConfigs(params: PageParams) {
  return listPage<ConfigRow>('/system/configs', params)
}

export function createConfig(payload: ConfigCreatePayload) {
  return createResource<ConfigRow, ConfigCreatePayload>('/system/configs', payload)
}

export function updateConfig(id: number, payload: ConfigUpdatePayload) {
  return updateResource<ConfigRow, ConfigUpdatePayload>(`/system/configs/${id}`, payload)
}

export function deleteConfig(id: number) {
  return deleteResource(`/system/configs/${id}`)
}

export function listLoginLogs(params: PageParams) {
  return listPage<LoginLogRow>('/system/login-logs', params)
}

export function listOperationLogs(params: PageParams) {
  return listPage<OperationLogRow>('/system/operation-logs', params)
}
