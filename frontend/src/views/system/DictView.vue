<script setup lang="ts">
import {
  createDictType,
  deleteDictType,
  listDictTypes,
  updateDictType,
  type DictTypePayload,
  type DictTypeUpdatePayload
} from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import SystemCrudPage, { type CrudField } from '@/components/SystemCrudPage.vue'

const columns: PageTableColumn[] = [
  { type: 'index', label: '#', width: 58, align: 'center' },
  { prop: 'code', label: '字典编码', minWidth: 180 },
  { prop: 'name', label: '字典名称', minWidth: 180 },
  { prop: 'status', label: '状态', width: 100, align: 'center', slot: 'status' }
]

const fields: CrudField[] = [
  { key: 'code', label: '字典编码', required: true },
  { key: 'name', label: '字典名称', required: true },
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
  return createDictType(payload as unknown as DictTypePayload)
}

function update(id: number, payload: Record<string, unknown>) {
  return updateDictType(id, payload as unknown as DictTypeUpdatePayload)
}
</script>

<template>
  <SystemCrudPage
    title="字典管理"
    description="维护系统字典类型，供业务表单和状态展示复用。"
    create-button-text="新增字典"
    :columns="columns"
    :loader="listDictTypes"
    :create="create"
    :update="update"
    :remove="deleteDictType"
    :fields="fields"
    :permissions="{
      create: 'system:dict:create',
      update: 'system:dict:update',
      delete: 'system:dict:delete'
    }"
  />
</template>
