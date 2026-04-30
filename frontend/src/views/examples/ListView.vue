<script setup lang="ts">
import { Delete, Download, Search } from '@element-plus/icons-vue'
import { computed, reactive, ref } from 'vue'

interface ExampleOrder {
  id: number
  code: string
  owner: string
  status: 'draft' | 'running' | 'done'
  amount: number
  updated_at: string
}

const filters = reactive({
  keyword: '',
  status: ''
})
const page = ref(1)
const pageSize = ref(10)
const selectedRows = ref<ExampleOrder[]>([])

const rows: ExampleOrder[] = Array.from({ length: 38 }, (_, index) => ({
  id: index + 1,
  code: `WO-${String(index + 1).padStart(4, '0')}`,
  owner: ['张三', '李四', '王五', '赵六'][index % 4],
  status: ['draft', 'running', 'done'][index % 3] as ExampleOrder['status'],
  amount: 1200 + index * 86,
  updated_at: `2026-04-${String((index % 28) + 1).padStart(2, '0')} 10:30`
}))

const statusText: Record<ExampleOrder['status'], string> = {
  draft: '草稿',
  running: '处理中',
  done: '已完成'
}

function getStatusText(status: ExampleOrder['status']) {
  return statusText[status]
}

function getStatusType(status: ExampleOrder['status']) {
  return status === 'done' ? 'success' : status === 'running' ? 'warning' : 'info'
}

const filteredRows = computed(() => {
  const keyword = filters.keyword.trim().toLowerCase()

  return rows.filter(row => {
    const matchedKeyword =
      !keyword ||
      row.code.toLowerCase().includes(keyword) ||
      row.owner.toLowerCase().includes(keyword)
    const matchedStatus = !filters.status || row.status === filters.status

    return matchedKeyword && matchedStatus
  })
})

const pagedRows = computed(() => {
  const start = (page.value - 1) * pageSize.value

  return filteredRows.value.slice(start, start + pageSize.value)
})

function resetPage() {
  page.value = 1
}
</script>

<template>
  <div class="oa-page">
    <header class="oa-page__header">
      <div>
        <h1 class="oa-page__title">列表示例</h1>
        <p class="oa-page__desc">展示筛选、表格分页、行选择和批量操作的典型后台列表。</p>
      </div>
      <div class="oa-page__toolbar">
        <ElButton :icon="Download">导出</ElButton>
        <ElButton :disabled="selectedRows.length === 0" :icon="Delete" type="danger" plain>
          批量删除 {{ selectedRows.length || '' }}
        </ElButton>
      </div>
    </header>

    <section class="example-filter">
      <ElInput
        v-model="filters.keyword"
        clearable
        placeholder="搜索工单号或负责人"
        :prefix-icon="Search"
        @clear="resetPage"
        @input="resetPage"
      />
      <ElSelect v-model="filters.status" clearable placeholder="状态" @change="resetPage">
        <ElOption label="草稿" value="draft" />
        <ElOption label="处理中" value="running" />
        <ElOption label="已完成" value="done" />
      </ElSelect>
    </section>

    <ElTable
      :data="pagedRows"
      border
      stripe
      row-key="id"
      @selection-change="selectedRows = $event"
    >
      <ElTableColumn type="selection" width="48" />
      <ElTableColumn prop="code" label="工单号" min-width="140" />
      <ElTableColumn prop="owner" label="负责人" min-width="120" />
      <ElTableColumn prop="amount" label="金额" min-width="120">
        <template #default="{ row }">￥{{ row.amount.toLocaleString() }}</template>
      </ElTableColumn>
      <ElTableColumn prop="status" label="状态" min-width="120">
        <template #default="{ row }">
          <ElTag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </ElTag>
        </template>
      </ElTableColumn>
      <ElTableColumn prop="updated_at" label="更新时间" min-width="170" />
    </ElTable>

    <div class="example-pagination">
      <ElPagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        background
        layout="total, sizes, prev, pager, next"
        :page-sizes="[10, 20, 50]"
        :total="filteredRows.length"
      />
    </div>
  </div>
</template>

<style scoped>
.example-filter {
  display: grid;
  grid-template-columns: minmax(220px, 320px) 180px;
  gap: 12px;
  margin-bottom: 16px;
}

.example-pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

@media (max-width: 768px) {
  .example-filter {
    grid-template-columns: 1fr;
  }
}
</style>
