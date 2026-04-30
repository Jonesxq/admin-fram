<script setup lang="ts">
import {
  createRole,
  deleteRole,
  listRoles,
  updateRole,
  type RolePayload,
  type RoleUpdatePayload
} from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import SystemCrudPage, { type CrudField } from '@/components/SystemCrudPage.vue'

const columns: PageTableColumn[] = [
  { type: 'index', label: '#', width: 58, align: 'center' },
  { prop: 'code', label: '角色编码', minWidth: 150 },
  { prop: 'name', label: '角色名称', minWidth: 150 },
  { prop: 'data_scope', label: '数据范围', minWidth: 140 },
  { prop: 'sort', label: '排序', width: 90, align: 'center' },
  { prop: 'status', label: '状态', width: 100, align: 'center', slot: 'status' }
]

const fields: CrudField[] = [
  { key: 'code', label: '角色编码', required: true },
  { key: 'name', label: '角色名称', required: true },
  {
    key: 'data_scope',
    label: '数据范围',
    type: 'select',
    defaultValue: 'all',
    required: true,
    options: [
      { label: '全部数据', value: 'all' },
      { label: '本部门', value: 'dept' },
      { label: '本人数据', value: 'self' }
    ]
  },
  { key: 'sort', label: '排序', type: 'number', defaultValue: 0 },
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
  return createRole(payload as unknown as RolePayload)
}

function update(id: number, payload: Record<string, unknown>) {
  return updateRole(id, payload as unknown as RoleUpdatePayload)
}
</script>

<template>
  <SystemCrudPage
    title="角色管理"
    description="维护角色编码、数据权限范围和启停状态。"
    create-button-text="新增角色"
    :columns="columns"
    :loader="listRoles"
    :create="create"
    :update="update"
    :remove="deleteRole"
    :fields="fields"
    :permissions="{
      create: 'system:role:create',
      update: 'system:role:update',
      delete: 'system:role:delete'
    }"
  />
</template>
