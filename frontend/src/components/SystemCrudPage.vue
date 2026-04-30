<script setup lang="ts">
import { Delete, Edit, Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { computed, reactive, ref } from 'vue'

import type { PageParams, PageResult } from '@/api/system'
import PageTable, { type PageTableColumn } from '@/components/PageTable.vue'
import PermissionButton from '@/components/PermissionButton.vue'
import StatusTag from '@/components/StatusTag.vue'

type CrudMode = 'create' | 'edit'
type RowData = Record<string, unknown>

export interface CrudFieldOption {
  label: string
  value: string | number
}

export interface CrudField {
  key: string
  label: string
  type?: 'input' | 'password' | 'textarea' | 'number' | 'select'
  required?: boolean
  requiredOnCreate?: boolean
  requiredOnUpdate?: boolean
  placeholder?: string
  options?: CrudFieldOption[]
  defaultValue?: string | number | null
  hideOnCreate?: boolean
  hideOnEdit?: boolean
  omitEmptyOnCreate?: boolean
  omitEmptyOnUpdate?: boolean
  emptyAsNull?: boolean
  min?: number
}

const props = defineProps<{
  title: string
  description: string
  columns: PageTableColumn[]
  loader: (params: PageParams) => Promise<PageResult<unknown>>
  create: (payload: RowData) => Promise<unknown>
  update: (id: number, payload: RowData) => Promise<unknown>
  remove: (id: number) => Promise<unknown>
  fields: CrudField[]
  permissions: {
    create: string
    update: string
    delete: string
  }
  rowKey?: string
  createButtonText?: string
}>()

const tableRef = ref<InstanceType<typeof PageTable> | null>(null)
const dialogVisible = ref(false)
const submitting = ref(false)
const mode = ref<CrudMode>('create')
const editingId = ref<number | null>(null)
const form = reactive<RowData>({})

const tableColumns = computed<PageTableColumn[]>(() => [
  ...props.columns,
  {
    label: '操作',
    width: 150,
    align: 'center',
    fixed: 'right',
    slot: 'row-actions'
  }
])

const visibleFields = computed(() =>
  props.fields.filter(field => {
    if (mode.value === 'create') {
      return !field.hideOnCreate
    }

    return !field.hideOnEdit
  })
)

const dialogTitle = computed(() => (mode.value === 'create' ? props.createButtonText ?? '新增' : '编辑'))

function fieldDefault(field: CrudField) {
  if (field.defaultValue !== undefined) {
    return field.defaultValue
  }

  return field.type === 'number' ? 0 : ''
}

function resetForm(nextMode: CrudMode, row?: RowData) {
  mode.value = nextMode
  editingId.value = typeof row?.id === 'number' ? row.id : null

  for (const field of props.fields) {
    form[field.key] = nextMode === 'edit' && row ? row[field.key] ?? fieldDefault(field) : fieldDefault(field)
  }
}

function openCreate() {
  resetForm('create')
  dialogVisible.value = true
}

function openEdit(row: RowData) {
  resetForm('edit', row)
  dialogVisible.value = true
}

function isRequired(field: CrudField) {
  if (mode.value === 'create' && field.requiredOnCreate !== undefined) {
    return field.requiredOnCreate
  }

  if (mode.value === 'edit' && field.requiredOnUpdate !== undefined) {
    return field.requiredOnUpdate
  }

  return field.required ?? false
}

function hasValue(value: unknown) {
  return value !== undefined && value !== null && String(value).trim() !== ''
}

function buildPayload() {
  const payload: RowData = {}

  for (const field of visibleFields.value) {
    let value = form[field.key]

    if (isRequired(field) && !hasValue(value)) {
      throw new Error(`请填写${field.label}`)
    }

    if (mode.value === 'create' && field.omitEmptyOnCreate && !hasValue(value)) {
      continue
    }

    if (mode.value === 'edit' && field.omitEmptyOnUpdate && !hasValue(value)) {
      continue
    }

    if (field.emptyAsNull && !hasValue(value)) {
      value = null
    }

    payload[field.key] = value
  }

  return payload
}

async function submitForm() {
  let payload: RowData

  try {
    payload = buildPayload()
  } catch (error) {
    ElMessage.warning(error instanceof Error ? error.message : '请完善表单')
    return
  }

  submitting.value = true

  try {
    if (mode.value === 'create') {
      await props.create(payload)
      ElMessage.success('新增成功')
    } else if (editingId.value !== null) {
      await props.update(editingId.value, payload)
      ElMessage.success('保存成功')
    }

    dialogVisible.value = false
    await tableRef.value?.reload()
  } catch {
    ElMessage.error(mode.value === 'create' ? '新增失败，请稍后重试' : '保存失败，请稍后重试')
  } finally {
    submitting.value = false
  }
}

async function confirmDelete(row: RowData) {
  if (typeof row.id !== 'number') {
    return
  }

  try {
    await ElMessageBox.confirm('确认删除该记录？', '删除确认', {
      type: 'warning',
      confirmButtonText: '删除',
      cancelButtonText: '取消'
    })
    await props.remove(row.id)
    ElMessage.success('删除成功')
    await tableRef.value?.reload()
  } catch (error) {
    if (error !== 'cancel' && error !== 'close') {
      ElMessage.error('删除失败，请稍后重试')
    }
  }
}
</script>

<template>
  <div class="oa-page">
    <header class="oa-page__header">
      <div>
        <h1 class="oa-page__title">{{ title }}</h1>
        <p class="oa-page__desc">{{ description }}</p>
      </div>
    </header>

    <PageTable
      ref="tableRef"
      :columns="tableColumns"
      :loader="loader"
      :row-key="rowKey ?? 'id'"
      :searchable="false"
    >
      <template #actions>
        <PermissionButton
          :permission="permissions.create"
          :icon="Plus"
          data-testid="crud-create-button"
          @click="openCreate"
        >
          {{ createButtonText ?? '新增' }}
        </PermissionButton>
      </template>

      <template #status="{ row }">
        <StatusTag :value="row.status" />
      </template>

      <template #type="{ row }">
        <ElTag effect="plain">{{ row.type }}</ElTag>
      </template>

      <template #row-actions="{ row }">
        <div class="system-crud__row-actions">
          <PermissionButton
            :permission="permissions.update"
            :icon="Edit"
            link
            type="primary"
            @click="openEdit(row)"
          >
            编辑
          </PermissionButton>
          <PermissionButton
            :permission="permissions.delete"
            :icon="Delete"
            link
            type="danger"
            @click="confirmDelete(row)"
          >
            删除
          </PermissionButton>
        </div>
      </template>
    </PageTable>

    <ElDialog v-model="dialogVisible" :title="dialogTitle" width="520px" destroy-on-close>
      <ElForm label-width="96px" class="system-crud__form" @submit.prevent>
        <ElFormItem
          v-for="field in visibleFields"
          :key="field.key"
          :label="field.label"
          :required="isRequired(field)"
        >
          <div class="system-crud__field" :data-testid="`field-${field.key}`">
            <ElInputNumber
              v-if="field.type === 'number'"
              v-model="form[field.key]"
              :min="field.min ?? 0"
              controls-position="right"
            />
            <ElSelect
              v-else-if="field.type === 'select'"
              v-model="form[field.key]"
              :placeholder="field.placeholder ?? `请选择${field.label}`"
            >
              <ElOption
                v-for="option in field.options"
                :key="String(option.value)"
                :label="option.label"
                :value="option.value"
              />
            </ElSelect>
            <ElInput
              v-else
              v-model="form[field.key]"
              :placeholder="field.placeholder ?? `请输入${field.label}`"
              :rows="field.type === 'textarea' ? 3 : undefined"
              :show-password="field.type === 'password'"
              :type="field.type === 'textarea' ? 'textarea' : field.type === 'password' ? 'password' : 'text'"
            />
          </div>
        </ElFormItem>
      </ElForm>
      <template #footer>
        <ElButton @click="dialogVisible = false">取消</ElButton>
        <ElButton
          type="primary"
          :loading="submitting"
          data-testid="crud-submit"
          @click="submitForm"
        >
          保存
        </ElButton>
      </template>
    </ElDialog>
  </div>
</template>

<style scoped>
.system-crud__row-actions {
  display: inline-flex;
  gap: 4px;
  align-items: center;
}

.system-crud__form {
  padding-top: 4px;
}

.system-crud__field {
  width: 100%;
}

.system-crud__form :deep(.el-input-number),
.system-crud__form :deep(.el-select) {
  width: 100%;
}
</style>
