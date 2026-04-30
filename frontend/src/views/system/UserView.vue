<script setup lang="ts">
import {
  createUser,
  deleteUser,
  listUsers,
  updateUser,
  type UserCreatePayload,
  type UserUpdatePayload
} from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import SystemCrudPage, { type CrudField } from '@/components/SystemCrudPage.vue'

const columns: PageTableColumn[] = [
  { type: 'index', label: '#', width: 58, align: 'center' },
  { prop: 'username', label: '用户名', minWidth: 140 },
  { prop: 'nickname', label: '昵称', minWidth: 140 },
  { prop: 'email', label: '邮箱', minWidth: 180 },
  { prop: 'mobile', label: '手机号', minWidth: 140 },
  { prop: 'dept_id', label: '部门ID', width: 100, align: 'center' },
  { prop: 'status', label: '状态', width: 100, align: 'center', slot: 'status' },
  { prop: 'last_login_at', label: '最后登录', minWidth: 180 }
]

const fields: CrudField[] = [
  { key: 'username', label: '用户名', requiredOnCreate: true, hideOnEdit: true },
  { key: 'password', label: '密码', type: 'password', requiredOnCreate: true, hideOnEdit: true },
  { key: 'nickname', label: '昵称', required: true },
  { key: 'email', label: '邮箱', omitEmptyOnCreate: true, omitEmptyOnUpdate: true },
  { key: 'mobile', label: '手机号', omitEmptyOnCreate: true, omitEmptyOnUpdate: true },
  {
    key: 'dept_id',
    label: '部门ID',
    type: 'number',
    defaultValue: null,
    emptyAsNull: true,
    omitEmptyOnCreate: true,
    omitEmptyOnUpdate: true,
    min: 1
  },
  {
    key: 'status',
    label: '状态',
    type: 'select',
    defaultValue: 'enabled',
    required: true,
    options: [
      { label: '启用', value: 'enabled' },
      { label: '停用', value: 'disabled' }
    ]
  }
]

function create(payload: Record<string, unknown>) {
  return createUser(payload as unknown as UserCreatePayload)
}

function update(id: number, payload: Record<string, unknown>) {
  return updateUser(id, payload as unknown as UserUpdatePayload)
}
</script>

<template>
  <SystemCrudPage
    title="用户管理"
    description="维护后台账号、联系方式、部门归属和登录状态。"
    create-button-text="新增用户"
    :columns="columns"
    :loader="listUsers"
    :create="create"
    :update="update"
    :remove="deleteUser"
    :fields="fields"
    :permissions="{
      create: 'system:user:create',
      update: 'system:user:update',
      delete: 'system:user:delete'
    }"
  />
</template>
