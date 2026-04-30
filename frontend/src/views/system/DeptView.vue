<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

import { listDepts } from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import PageTable from '@/components/PageTable.vue'
import PermissionButton from '@/components/PermissionButton.vue'

const columns: PageTableColumn[] = [
  { prop: 'name', label: '部门名称', minWidth: 180 },
  { prop: 'parent_id', label: '上级ID', width: 100, align: 'center' },
  { prop: 'ancestors', label: '祖级路径', minWidth: 180 },
  { prop: 'sort', label: '排序', width: 90, align: 'center' },
  { prop: 'status', label: '状态', width: 100, align: 'center', slot: 'status' }
]

function showPendingMessage() {
  ElMessage.info('新增部门写接口将在后续任务接入')
}
</script>

<template>
  <div class="oa-page">
    <header class="oa-page__header">
      <div>
        <h1 class="oa-page__title">部门管理</h1>
        <p class="oa-page__desc">查看组织层级、排序和部门状态。</p>
      </div>
      <PermissionButton permission="system:dept:create" :icon="Plus" @click="showPendingMessage">
        新增部门
      </PermissionButton>
    </header>

    <PageTable :columns="columns" :loader="listDepts" row-key="id">
      <template #status="{ row }">
        <ElTag :type="String(row.status) === '1' ? 'success' : 'info'" effect="light">
          {{ String(row.status) === '1' ? '启用' : '停用' }}
        </ElTag>
      </template>
    </PageTable>
  </div>
</template>
