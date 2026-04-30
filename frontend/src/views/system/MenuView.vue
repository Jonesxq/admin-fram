<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

import { listMenus } from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import PageTable from '@/components/PageTable.vue'
import PermissionButton from '@/components/PermissionButton.vue'

const columns: PageTableColumn[] = [
  { prop: 'title', label: '菜单名称', minWidth: 160 },
  { prop: 'type', label: '类型', width: 100, align: 'center', slot: 'type' },
  { prop: 'path', label: '路由路径', minWidth: 170 },
  { prop: 'component', label: '组件', minWidth: 180 },
  { prop: 'permission', label: '权限标识', minWidth: 190 },
  { prop: 'icon', label: '图标', width: 110 },
  { prop: 'sort', label: '排序', width: 80, align: 'center' },
  { prop: 'status', label: '状态', width: 100, align: 'center', slot: 'status' }
]

function showPendingMessage() {
  ElMessage.info('新增菜单写接口将在后续任务接入')
}
</script>

<template>
  <div class="oa-page">
    <header class="oa-page__header">
      <div>
        <h1 class="oa-page__title">菜单管理</h1>
        <p class="oa-page__desc">维护菜单、按钮权限和前端组件映射。</p>
      </div>
      <PermissionButton permission="system:menu:create" :icon="Plus" @click="showPendingMessage">
        新增菜单
      </PermissionButton>
    </header>

    <PageTable :columns="columns" :loader="listMenus" row-key="id" :searchable="false">
      <template #type="{ row }">
        <ElTag effect="plain">{{ row.type }}</ElTag>
      </template>
      <template #status="{ row }">
        <ElTag :type="String(row.status) === '1' ? 'success' : 'info'" effect="light">
          {{ String(row.status) === '1' ? '启用' : '停用' }}
        </ElTag>
      </template>
    </PageTable>
  </div>
</template>
