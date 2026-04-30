<script setup lang="ts">
import {
  createDept,
  deleteDept,
  listDepts,
  updateDept,
  type DeptPayload,
  type DeptUpdatePayload
} from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import SystemCrudPage, { type CrudField } from '@/components/SystemCrudPage.vue'

const columns: PageTableColumn[] = [
  { prop: 'name', label: '部门名称', minWidth: 180 },
  { prop: 'parent_id', label: '上级ID', width: 100, align: 'center' },
  { prop: 'ancestors', label: '祖级路径', minWidth: 180 },
  { prop: 'sort', label: '排序', width: 90, align: 'center' },
  { prop: 'status', label: '状态', width: 100, align: 'center', slot: 'status' }
]

const fields: CrudField[] = [
  { key: 'name', label: '部门名称', required: true },
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
  { key: 'ancestors', label: '祖级路径', defaultValue: '', omitEmptyOnCreate: true },
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
  return createDept(payload as unknown as DeptPayload)
}

function update(id: number, payload: Record<string, unknown>) {
  return updateDept(id, payload as unknown as DeptUpdatePayload)
}
</script>

<template>
  <SystemCrudPage
    title="部门管理"
    description="维护组织层级、排序和部门状态。"
    create-button-text="新增部门"
    :columns="columns"
    :loader="listDepts"
    :create="create"
    :update="update"
    :remove="deleteDept"
    :fields="fields"
    :permissions="{
      create: 'system:dept:create',
      update: 'system:dept:update',
      delete: 'system:dept:delete'
    }"
  />
</template>
