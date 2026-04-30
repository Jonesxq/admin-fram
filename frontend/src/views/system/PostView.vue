<script setup lang="ts">
import {
  createPost,
  deletePost,
  listPosts,
  updatePost,
  type PostPayload,
  type PostUpdatePayload
} from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import SystemCrudPage, { type CrudField } from '@/components/SystemCrudPage.vue'

const columns: PageTableColumn[] = [
  { type: 'index', label: '#', width: 58, align: 'center' },
  { prop: 'code', label: '岗位编码', minWidth: 150 },
  { prop: 'name', label: '岗位名称', minWidth: 160 },
  { prop: 'sort', label: '排序', width: 90, align: 'center' },
  { prop: 'status', label: '状态', width: 100, align: 'center', slot: 'status' }
]

const fields: CrudField[] = [
  { key: 'code', label: '岗位编码', required: true },
  { key: 'name', label: '岗位名称', required: true },
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
  return createPost(payload as unknown as PostPayload)
}

function update(id: number, payload: Record<string, unknown>) {
  return updatePost(id, payload as unknown as PostUpdatePayload)
}
</script>

<template>
  <SystemCrudPage
    title="岗位管理"
    description="管理岗位编码、名称、排序和状态。"
    create-button-text="新增岗位"
    :columns="columns"
    :loader="listPosts"
    :create="create"
    :update="update"
    :remove="deletePost"
    :fields="fields"
    :permissions="{
      create: 'system:post:create',
      update: 'system:post:update',
      delete: 'system:post:delete'
    }"
  />
</template>
