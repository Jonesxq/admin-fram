<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

import { listUsers } from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import PageTable from '@/components/PageTable.vue'
import PermissionButton from '@/components/PermissionButton.vue'

const columns: PageTableColumn[] = [
  { type: 'index', label: '#', width: 58, align: 'center' },
  { prop: 'username', label: '用户名', minWidth: 140 },
  { prop: 'nickname', label: '昵称', minWidth: 140 },
  { prop: 'email', label: '邮箱', minWidth: 180 },
  { prop: 'mobile', label: '手机号', minWidth: 140 },
  { prop: 'dept_id', label: '部门ID', width: 100, align: 'center' },
  { prop: 'status', label: '状态', width: 100, align: 'center', slot: 'status' },
  { prop: 'last_login_at', label: '最后登录', minWidth: 180 }
]

function showPendingMessage() {
  ElMessage.info('新增用户写接口将在后续任务接入')
}
</script>

<template>
  <div class="oa-page">
    <header class="oa-page__header">
      <div>
        <h1 class="oa-page__title">用户管理</h1>
        <p class="oa-page__desc">维护后台账号、联系方式、部门归属和登录状态。</p>
      </div>
      <PermissionButton permission="system:user:create" :icon="Plus" @click="showPendingMessage">
        新增用户
      </PermissionButton>
    </header>

    <PageTable :columns="columns" :loader="listUsers" row-key="id">
      <template #status="{ row }">
        <ElTag :type="String(row.status) === '1' ? 'success' : 'info'" effect="light">
          {{ String(row.status) === '1' ? '启用' : '停用' }}
        </ElTag>
      </template>
    </PageTable>
  </div>
</template>
