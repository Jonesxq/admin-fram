<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

import { listPosts } from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import PageTable from '@/components/PageTable.vue'
import PermissionButton from '@/components/PermissionButton.vue'

const columns: PageTableColumn[] = [
  { type: 'index', label: '#', width: 58, align: 'center' },
  { prop: 'code', label: '岗位编码', minWidth: 150 },
  { prop: 'name', label: '岗位名称', minWidth: 160 },
  { prop: 'sort', label: '排序', width: 90, align: 'center' },
  { prop: 'status', label: '状态', width: 100, align: 'center', slot: 'status' }
]

function showPendingMessage() {
  ElMessage.info('新增岗位写接口将在后续任务接入')
}
</script>

<template>
  <div class="oa-page">
    <header class="oa-page__header">
      <div>
        <h1 class="oa-page__title">岗位管理</h1>
        <p class="oa-page__desc">管理岗位编码、名称、排序和状态。</p>
      </div>
      <PermissionButton permission="system:post:create" :icon="Plus" @click="showPendingMessage">
        新增岗位
      </PermissionButton>
    </header>

    <PageTable :columns="columns" :loader="listPosts" row-key="id" :searchable="false">
      <template #status="{ row }">
        <ElTag :type="String(row.status) === '1' ? 'success' : 'info'" effect="light">
          {{ String(row.status) === '1' ? '启用' : '停用' }}
        </ElTag>
      </template>
    </PageTable>
  </div>
</template>
