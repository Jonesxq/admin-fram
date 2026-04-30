<script setup lang="ts">
import {
  createMenu,
  deleteMenu,
  listMenus,
  updateMenu,
  type MenuPayload,
  type MenuUpdatePayload
} from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import SystemCrudPage, { type CrudField } from '@/components/SystemCrudPage.vue'

const columns: PageTableColumn[] = [
  { prop: 'title', label: '菜单名称', minWidth: 160 },
  { prop: 'type', label: '类型', width: 100, align: 'center', slot: 'type' },
  { prop: 'path', label: '路由路径', minWidth: 170 },
  { prop: 'component', label: '组件', minWidth: 180 },
  { prop: 'permission', label: '权限标识', minWidth: 190 },
  { prop: 'icon', label: '图标', width: 110 },
  { prop: 'sort', label: '排序', width: 80, align: 'center' },
  { prop: 'status', label: '状态', width: 100, align: 'center', slot: 'status' }
]

const fields: CrudField[] = [
  {
    key: 'type',
    label: '类型',
    type: 'select',
    defaultValue: 'menu',
    required: true,
    options: [
      { label: '目录', value: 'catalog' },
      { label: '菜单', value: 'menu' },
      { label: '按钮', value: 'button' }
    ]
  },
  { key: 'title', label: '菜单名称', required: true },
  {
    key: 'parent_id',
    label: '上级ID',
    type: 'number',
    defaultValue: null,
    emptyAsNull: true,
    omitEmptyOnCreate: true,
    omitEmptyOnUpdate: true,
    min: 1
  },
  { key: 'path', label: '路由路径', omitEmptyOnCreate: true, omitEmptyOnUpdate: true },
  { key: 'component', label: '组件', omitEmptyOnCreate: true, omitEmptyOnUpdate: true },
  { key: 'permission', label: '权限标识', omitEmptyOnCreate: true, omitEmptyOnUpdate: true },
  { key: 'icon', label: '图标', omitEmptyOnCreate: true, omitEmptyOnUpdate: true },
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
  return createMenu(payload as unknown as MenuPayload)
}

function update(id: number, payload: Record<string, unknown>) {
  return updateMenu(id, payload as unknown as MenuUpdatePayload)
}
</script>

<template>
  <SystemCrudPage
    title="菜单管理"
    description="维护菜单、按钮权限和前端组件映射。"
    create-button-text="新增菜单"
    :columns="columns"
    :loader="listMenus"
    :create="create"
    :update="update"
    :remove="deleteMenu"
    :fields="fields"
    :permissions="{
      create: 'system:menu:create',
      update: 'system:menu:update',
      delete: 'system:menu:delete'
    }"
  />
</template>
