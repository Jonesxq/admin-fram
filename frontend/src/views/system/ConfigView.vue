<script setup lang="ts">
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

import { listConfigs } from '@/api/system'
import type { PageTableColumn } from '@/components/PageTable.vue'
import PageTable from '@/components/PageTable.vue'
import PermissionButton from '@/components/PermissionButton.vue'

const columns: PageTableColumn[] = [
  { type: 'index', label: '#', width: 58, align: 'center' },
  { prop: 'key', label: '参数键名', minWidth: 210 },
  { prop: 'name', label: '参数名称', minWidth: 180 },
  { prop: 'remark', label: '备注', minWidth: 260 }
]

function showPendingMessage() {
  ElMessage.info('新增参数写接口将在后续任务接入')
}
</script>

<template>
  <div class="oa-page">
    <header class="oa-page__header">
      <div>
        <h1 class="oa-page__title">参数配置</h1>
        <p class="oa-page__desc">集中查看系统运行参数和业务配置说明。</p>
      </div>
      <PermissionButton permission="system:config:create" :icon="Plus" @click="showPendingMessage">
        新增参数
      </PermissionButton>
    </header>

    <PageTable :columns="columns" :loader="listConfigs" row-key="id" :searchable="false" />
  </div>
</template>
