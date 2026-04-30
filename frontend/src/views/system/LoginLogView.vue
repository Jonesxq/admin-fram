<script setup lang="ts">
import { Download } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

import { listLoginLogs } from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import PageTable from '@/components/PageTable.vue'
import PermissionButton from '@/components/PermissionButton.vue'

const columns: PageTableColumn[] = [
  { prop: 'username', label: '用户名', minWidth: 130 },
  { prop: 'success', label: '结果', width: 100, align: 'center', slot: 'success' },
  { prop: 'message', label: '消息', minWidth: 180 },
  { prop: 'ip_address', label: 'IP地址', minWidth: 150 },
  { prop: 'user_agent', label: '客户端', minWidth: 260 },
  { prop: 'created_at', label: '登录时间', minWidth: 180 }
]

function showPendingMessage() {
  ElMessage.info('日志导出将在后续任务接入')
}
</script>

<template>
  <div class="oa-page">
    <header class="oa-page__header">
      <div>
        <h1 class="oa-page__title">登录日志</h1>
        <p class="oa-page__desc">追踪登录来源、登录结果和客户端信息。</p>
      </div>
      <PermissionButton permission="system:login-log:list" :icon="Download" plain @click="showPendingMessage">
        导出日志
      </PermissionButton>
    </header>

    <PageTable :columns="columns" :loader="listLoginLogs" row-key="id">
      <template #success="{ row }">
        <ElTag :type="row.success ? 'success' : 'danger'" effect="light">
          {{ row.success ? '成功' : '失败' }}
        </ElTag>
      </template>
    </PageTable>
  </div>
</template>
