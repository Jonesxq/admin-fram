<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { onMounted, ref } from 'vue'

import type { PageParams, PageResult } from '@/api/system'

export interface PageTableColumn<T = Record<string, unknown>> {
  prop?: keyof T | string
  label?: string
  width?: string | number
  minWidth?: string | number
  align?: 'left' | 'center' | 'right'
  fixed?: true | 'left' | 'right'
  formatter?: (row: T) => string | number
  slot?: string
  type?: 'selection' | 'index'
}

const props = withDefaults(
  defineProps<{
    columns: PageTableColumn[]
    loader: (params: PageParams) => Promise<PageResult<unknown>>
    rowKey: string
    keywordPlaceholder?: string
    searchable?: boolean
  }>(),
  {
    keywordPlaceholder: '请输入关键词',
    searchable: false
  }
)

const rows = ref<unknown[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const keyword = ref('')
const loading = ref(false)
const latestRequestId = ref(0)

async function loadData() {
  const requestId = latestRequestId.value + 1

  latestRequestId.value = requestId
  loading.value = true

  try {
    const result = await props.loader({
      page: page.value,
      page_size: pageSize.value,
      keyword: keyword.value.trim() || undefined
    })

    if (requestId !== latestRequestId.value) {
      return
    }

    rows.value = result.items
    total.value = result.total
    page.value = result.page
    pageSize.value = result.page_size
  } catch {
    if (requestId === latestRequestId.value) {
      ElMessage.error('列表加载失败，请稍后重试')
    }
  } finally {
    if (requestId === latestRequestId.value) {
      loading.value = false
    }
  }
}

function handleSearch() {
  page.value = 1
  void loadData()
}

function handleRefresh() {
  void loadData()
}

function handleSizeChange(size: number) {
  pageSize.value = size
  page.value = 1
  void loadData()
}

function handleCurrentChange(current: number) {
  page.value = current
  void loadData()
}

function formatCell(column: PageTableColumn, row: unknown) {
  if (column.formatter) {
    return column.formatter(row as Record<string, unknown>)
  }

  return column.prop ? ((row as Record<string, unknown>)[column.prop] ?? '-') : '-'
}

onMounted(() => {
  void loadData()
})

defineExpose({
  reload: loadData
})
</script>

<template>
  <section class="page-table">
    <div class="page-table__toolbar">
      <ElInput
        v-if="searchable"
        v-model="keyword"
        clearable
        class="page-table__search"
        :placeholder="keywordPlaceholder"
        @clear="handleSearch"
        @keyup.enter="handleSearch"
      />
      <ElButton v-if="searchable" type="primary" @click="handleSearch">查询</ElButton>
      <ElButton @click="handleRefresh">刷新</ElButton>
      <div class="page-table__actions">
        <slot name="actions" />
      </div>
    </div>

    <ElTable
      v-loading="loading"
      :data="rows"
      :row-key="rowKey"
      border
      stripe
      class="page-table__grid"
    >
      <ElTableColumn
        v-for="column in columns"
        :key="`${column.type ?? 'data'}-${String(column.prop ?? column.label)}`"
        :align="column.align"
        :fixed="column.fixed"
        :label="column.label"
        :min-width="column.minWidth"
        :prop="column.prop"
        :type="column.type"
        :width="column.width"
      >
        <template v-if="!column.type" #default="{ row }">
          <slot v-if="column.slot" :name="column.slot" :row="row" :column="column" />
          <span v-else>{{ formatCell(column, row) }}</span>
        </template>
      </ElTableColumn>
    </ElTable>

    <div class="page-table__pagination">
      <ElPagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        background
        layout="total, sizes, prev, pager, next, jumper"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        @current-change="handleCurrentChange"
        @size-change="handleSizeChange"
      />
    </div>
  </section>
</template>

<style scoped>
.page-table {
  display: flex;
  min-height: 0;
  flex-direction: column;
  gap: 14px;
}

.page-table__toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.page-table__search {
  width: min(320px, 100%);
}

.page-table__actions {
  display: flex;
  gap: 10px;
  margin-left: auto;
}

.page-table__grid {
  width: 100%;
}

.page-table__pagination {
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .page-table__actions {
    width: 100%;
    margin-left: 0;
  }

  .page-table__pagination {
    justify-content: flex-start;
    overflow-x: auto;
  }
}
</style>
