<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

import { listDictTypes } from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import PageTable from '@/components/PageTable.vue'
import PermissionButton from '@/components/PermissionButton.vue'

const columns: PageTableColumn[] = [
  { type: 'index', label: '#', width: 58, align: 'center' },
  { prop: 'code', label: '字典编码', minWidth: 180 },
  { prop: 'name', label: '字典名称', minWidth: 180 },
  { prop: 'status', label: '状态', width: 100, align: 'center', slot: 'status' }
]

function showPendingMessage() {
  ElMessage.info('新增字典写接口将在后续任务接入')
}
</script>

<template>
  <div class="oa-page">
    <header class="oa-page__header">
      <div>
        <h1 class="oa-page__title">字典管理</h1>
        <p class="oa-page__desc">维护系统字典类型，供业务表单和状态展示复用。</p>
      </div>
      <PermissionButton permission="system:dict:create" :icon="Plus" @click="showPendingMessage">
        新增字典
      </PermissionButton>
    </header>

    <PageTable :columns="columns" :loader="listDictTypes" row-key="id">
      <template #status="{ row }">
        <ElTag :type="String(row.status) === '1' ? 'success' : 'info'" effect="light">
          {{ String(row.status) === '1' ? '启用' : '停用' }}
        </ElTag>
      </template>
    </PageTable>
  </div>
</template>
