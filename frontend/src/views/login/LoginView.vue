<script setup lang="ts">
import { Lock, User } from '@element-plus/icons-vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules: FormRules<typeof form> = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

function redirectTarget() {
  return typeof route.query.redirect === 'string' && route.query.redirect
    ? route.query.redirect
    : '/dashboard'
}

async function handleLogin() {
  if (loading.value) {
    return
  }

  const valid = await formRef.value?.validate().catch(() => false)

  if (!valid) {
    return
  }

  loading.value = true

  try {
    await authStore.login({
      username: form.username.trim(),
      password: form.password
    })
    await router.replace(redirectTarget())
  } catch {
    ElMessage.error('登录失败，请检查用户名或密码')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="login-page">
    <section class="login-panel">
      <div class="login-panel__brand">
        <span class="login-panel__mark">OA</span>
        <div>
          <h1>后台管理系统</h1>
          <p>请使用管理员账号登录</p>
        </div>
      </div>

      <ElForm
        ref="formRef"
        :model="form"
        :rules="rules"
        class="login-form"
        label-position="top"
        @keyup.enter="handleLogin"
      >
        <ElFormItem label="用户名" prop="username">
          <div class="login-form__field" data-testid="login-username">
            <ElInput
              v-model="form.username"
              size="large"
              autocomplete="username"
              placeholder="请输入用户名"
              :prefix-icon="User"
            />
          </div>
        </ElFormItem>
        <ElFormItem label="密码" prop="password">
          <div class="login-form__field" data-testid="login-password">
            <ElInput
              v-model="form.password"
              size="large"
              type="password"
              show-password
              autocomplete="current-password"
              placeholder="请输入密码"
              :prefix-icon="Lock"
            />
          </div>
        </ElFormItem>
        <ElButton
          type="primary"
          size="large"
          class="login-form__submit"
          data-testid="login-submit"
          :loading="loading"
          @click="handleLogin"
        >
          登录
        </ElButton>
      </ElForm>
    </section>
  </main>
</template>

<style scoped>
.login-page {
  display: grid;
  min-height: 100vh;
  place-items: center;
  padding: 24px;
  background:
    linear-gradient(135deg, rgba(15, 118, 110, 0.12), transparent 34%),
    linear-gradient(315deg, rgba(37, 99, 235, 0.1), transparent 34%),
    #f6f8fb;
}

.login-panel {
  width: min(420px, 100%);
  padding: 32px;
  border: 1px solid #dfe5ee;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 22px 54px rgba(15, 23, 42, 0.12);
}

.login-panel__brand {
  display: flex;
  gap: 14px;
  align-items: center;
  margin-bottom: 28px;
}

.login-panel__mark {
  display: inline-grid;
  width: 48px;
  height: 48px;
  place-items: center;
  border-radius: 8px;
  background: #0f766e;
  color: #ffffff;
  font-weight: 800;
}

.login-panel__brand h1 {
  margin: 0;
  color: #111827;
  font-size: 22px;
  font-weight: 800;
  letter-spacing: 0;
}

.login-panel__brand p {
  margin: 4px 0 0;
  color: #6b7280;
  font-size: 13px;
}

.login-form {
  display: grid;
  gap: 4px;
}

.login-form__submit {
  width: 100%;
  margin-top: 8px;
}

.login-form__field {
  width: 100%;
}

@media (max-width: 480px) {
  .login-page {
    padding: 14px;
  }

  .login-panel {
    padding: 24px;
  }
}
</style>
