import { apiClient } from './client'

export interface LoginPayload {
  username: string
  password: string
}

export interface LoginResult {
  access_token: string
  token_type: string
}

export interface AuthUser {
  id: number
  username: string
  nickname: string
}

export interface AuthMenu {
  id: number
  parent_id: number | null
  type: string
  title: string
  path: string
  component: string | null
  permission: string | null
  icon: string | null
  sort: number
}

export interface MeResult {
  user: AuthUser
  roles: string[]
  permissions: string[]
  menus: AuthMenu[]
}

export async function loginApi(payload: LoginPayload): Promise<LoginResult> {
  const response = await apiClient.post('/auth/login', payload)

  return response.data.data
}

export async function meApi(): Promise<MeResult> {
  const response = await apiClient.get('/auth/me')

  return response.data.data
}
