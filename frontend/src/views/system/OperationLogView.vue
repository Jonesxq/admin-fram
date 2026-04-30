<script setup lang="ts">
import { Download } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

import { listOperationLogs } from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import PageTable from '@/components/PageTable.vue'
import PermissionButton from '@/components/PermissionButton.vue'

const columns: PageTableColumn[] = [
  { prop: 'title', label: '操作标题', minWidth: 160 },
  { prop: 'username', label: '操作人', minWidth: 130 },
  { prop: 'permission', label: '权限标识', minWidth: 190 },
  { prop: 'method', label: '方法', width: 90, align: 'center' },
  { prop: 'path', label: '请求路径', minWidth: 220 },
  { prop: 'ip_address', label: 'IP地址', minWidth: 140 },
  { prop: 'success', label: '结果', width: 100, align: 'center', slot: 'success' },
  { prop: 'message', label: '消息', minWidth: 180 },
  { prop: 'created_at', label: '操作时间', minWidth: 180 }
]

function showPendingMessage() {
  ElMessage.info('日志导出将在后续任务接入')
}
</script>

<template>
  <div class="oa-page">
    <header class="oa-page__header">
      <div>
        <h1 class="oa-page__title">操作日志</h1>
        <p class="oa-page__desc">查看后台关键操作、接口路径、权限标识和执行结果。</p>
      </div>
      <PermissionButton permission="system:operation-log:list" :icon="Download" plain @click="showPendingMessage">
        导出日志
      </PermissionButton>
    </header>

    <PageTable :columns="columns" :loader="listOperationLogs" row-key="id">
      <template #success="{ row }">
        <ElTag :type="row.success ? 'success' : 'danger'" effect="light">
          {{ row.success ? '成功' : '失败' }}
        </ElTag>
      </template>
    </PageTable>
  </div>
</template>
