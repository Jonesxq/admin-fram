<script setup lang="ts">
import {
  createConfig,
  deleteConfig,
  listConfigs,
  updateConfig,
  type ConfigCreatePayload,
  type ConfigUpdatePayload
} from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import SystemCrudPage, { type CrudField } from '@/components/SystemCrudPage.vue'

const columns: PageTableColumn[] = [
  { type: 'index', label: '#', width: 58, align: 'center' },
  { prop: 'key', label: '参数键名', minWidth: 210 },
  { prop: 'name', label: '参数名称', minWidth: 180 },
  { prop: 'remark', label: '备注', minWidth: 260 }
]

const fields: CrudField[] = [
  { key: 'key', label: '参数键名', required: true },
  {
    key: 'value',
    label: '参数值',
    type: 'textarea',
    requiredOnCreate: true,
    requiredOnUpdate: false,
    omitEmptyOnUpdate: true,
    placeholder: '编辑时留空则不更新参数值'
  },
  { key: 'name', label: '参数名称', required: true },
  { key: 'remark', label: '备注', type: 'textarea', omitEmptyOnCreate: true, omitEmptyOnUpdate: true }
]

function create(payload: Record<string, unknown>) {
  return createConfig(payload as unknown as ConfigCreatePayload)
}

function update(id: number, payload: Record<string, unknown>) {
  return updateConfig(id, payload as unknown as ConfigUpdatePayload)
}
</script>

<template>
  <SystemCrudPage
    title="参数配置"
    description="集中维护系统运行参数和业务配置说明。"
    create-button-text="新增参数"
    :columns="columns"
    :loader="listConfigs"
    :create="create"
    :update="update"
    :remove="deleteConfig"
    :fields="fields"
    :permissions="{
      create: 'system:config:create',
      update: 'system:config:update',
      delete: 'system:config:delete'
    }"
  />
</template>
