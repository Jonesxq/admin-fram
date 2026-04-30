<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

import { listRoles } from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import PageTable from '@/components/PageTable.vue'
import PermissionButton from '@/components/PermissionButton.vue'

const columns: PageTableColumn[] = [
  { type: 'index', label: '#', width: 58, align: 'center' },
  { prop: 'code', label: '角色编码', minWidth: 150 },
  { prop: 'name', label: '角色名称', minWidth: 150 },
  { prop: 'data_scope', label: '数据范围', minWidth: 140 },
  { prop: 'sort', label: '排序', width: 90, align: 'center' },
  { prop: 'status', label: '状态', width: 100, align: 'center', slot: 'status' }
]

function showPendingMessage() {
  ElMessage.info('新增角色写接口将在后续任务接入')
}
</script>

<template>
  <div class="oa-page">
    <header class="oa-page__header">
      <div>
        <h1 class="oa-page__title">角色管理</h1>
        <p class="oa-page__desc">查看角色编码、数据权限范围和启停状态。</p>
      </div>
      <PermissionButton permission="system:role:create" :icon="Plus" @click="showPendingMessage">
        新增角色
      </PermissionButton>
    </header>

    <PageTable :columns="columns" :loader="listRoles" row-key="id" :searchable="false">
      <template #status="{ row }">
        <ElTag :type="String(row.status) === '1' ? 'success' : 'info'" effect="light">
          {{ String(row.status) === '1' ? '启用' : '停用' }}
        </ElTag>
      </template>
    </PageTable>
  </div>
</template>
