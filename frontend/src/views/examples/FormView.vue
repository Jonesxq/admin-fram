<script setup lang="ts">
import { Check, RefreshLeft } from '@element-plus/icons-vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { reactive, ref } from 'vue'

interface ExampleForm {
  name: string
  owner: string
  priority: string
  dateRange: string[]
  budget: number
  description: string
  enabled: boolean
}

const formRef = ref<FormInstance>()
const form = reactive<ExampleForm>({
  name: '',
  owner: '',
  priority: 'normal',
  dateRange: [],
  budget: 3000,
  description: '',
  enabled: true
})

const rules: FormRules<ExampleForm> = {
  name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  owner: [{ required: true, message: '请选择负责人', trigger: 'change' }],
  dateRange: [{ required: true, message: '请选择起止日期', trigger: 'change' }],
  description: [{ required: true, min: 8, message: '说明至少 8 个字符', trigger: 'blur' }]
}

async function submitForm() {
  const valid = await formRef.value?.validate().catch(() => false)

  if (valid) {
    ElMessage.success('表单校验通过，写接口将在后续任务接入')
  }
}

function resetForm() {
  formRef.value?.resetFields()
}
</script>

<template>
  <div class="oa-page">
    <header class="oa-page__header">
      <div>
        <h1 class="oa-page__title">表单示例</h1>
        <p class="oa-page__desc">展示 Element Plus 表单布局、校验、开关和范围选择。</p>
      </div>
    </header>

    <ElForm
      ref="formRef"
      class="example-form"
      :model="form"
      :rules="rules"
      label-position="top"
      status-icon
    >
      <ElFormItem label="项目名称" prop="name">
        <ElInput v-model="form.name" maxlength="32" show-word-limit placeholder="请输入项目名称" />
      </ElFormItem>

      <ElFormItem label="负责人" prop="owner">
        <ElSelect v-model="form.owner" placeholder="请选择负责人">
          <ElOption label="张三" value="zhangsan" />
          <ElOption label="李四" value="lisi" />
          <ElOption label="王五" value="wangwu" />
        </ElSelect>
      </ElFormItem>

      <ElFormItem label="优先级" prop="priority">
        <ElRadioGroup v-model="form.priority">
          <ElRadioButton label="low">低</ElRadioButton>
          <ElRadioButton label="normal">普通</ElRadioButton>
          <ElRadioButton label="high">高</ElRadioButton>
        </ElRadioGroup>
      </ElFormItem>

      <ElFormItem label="起止日期" prop="dateRange">
        <ElDatePicker
          v-model="form.dateRange"
          type="daterange"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
        />
      </ElFormItem>

      <ElFormItem label="预算" prop="budget">
        <ElInputNumber v-model="form.budget" :min="0" :step="500" controls-position="right" />
      </ElFormItem>

      <ElFormItem label="启用流程">
        <ElSwitch v-model="form.enabled" active-text="启用" inactive-text="停用" />
      </ElFormItem>

      <ElFormItem class="example-form__wide" label="项目说明" prop="description">
        <ElInput
          v-model="form.description"
          type="textarea"
          :rows="5"
          maxlength="200"
          show-word-limit
          placeholder="请输入业务背景、目标和验收口径"
        />
      </ElFormItem>

      <div class="example-form__actions">
        <ElButton :icon="RefreshLeft" @click="resetForm">重置</ElButton>
        <ElButton type="primary" :icon="Check" @click="submitForm">提交校验</ElButton>
      </div>
    </ElForm>
  </div>
</template>

<style scoped>
.example-form {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 4px 18px;
  max-width: 920px;
}

.example-form__wide,
.example-form__actions {
  grid-column: 1 / -1;
}

.example-form__actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 8px;
}

@media (max-width: 768px) {
  .example-form {
    grid-template-columns: 1fr;
  }
}
</style>
