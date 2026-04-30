<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  Expand,
  Fold,
  FullScreen,
  SwitchButton,
  UserFilled,
  MagicStick
} from '@element-plus/icons-vue'

import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'

const appStore = useAppStore()
const authStore = useAuthStore()
const router = useRouter()

const username = computed(() => authStore.user?.nickname || authStore.user?.username || '管理员')

async function toggleFullscreen() {
  if (document.fullscreenElement) {
    await document.exitFullscreen()
    return
  }

  await document.documentElement.requestFullscreen()
}

async function logout() {
  authStore.logout()
  await router.push('/login')
}
</script>

<template>
  <header class="top-bar">
    <div class="top-bar__left">
      <ElButton
        circle
        text
        :icon="appStore.sidebarCollapsed ? Expand : Fold"
        aria-label="折叠菜单"
        @click="appStore.toggleSidebar()"
      />
      <span class="top-bar__title">后台管理</span>
    </div>

    <div class="top-bar__actions">
      <ElButton circle text :icon="FullScreen" aria-label="全屏" @click="toggleFullscreen" />
      <ElButton
        circle
        text
        :icon="MagicStick"
        aria-label="主题"
        @click="appStore.toggleThemePanel()"
      />

      <ElDropdown trigger="click">
        <button class="top-bar__user" type="button">
          <ElIcon><UserFilled /></ElIcon>
          <span>{{ username }}</span>
        </button>

        <template #dropdown>
          <ElDropdownMenu>
            <ElDropdownItem :icon="SwitchButton" @click="logout">退出登录</ElDropdownItem>
          </ElDropdownMenu>
        </template>
      </ElDropdown>
    </div>
  </header>
</template>

<style scoped>
.top-bar {
  display: flex;
  height: 56px;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid var(--oa-border);
  background: var(--oa-panel);
}

.top-bar__left,
.top-bar__actions,
.top-bar__user {
  display: flex;
  align-items: center;
}

.top-bar__left,
.top-bar__actions {
  gap: 8px;
}

.top-bar__title {
  font-size: 16px;
  font-weight: 700;
}

.top-bar__user {
  gap: 8px;
  height: 36px;
  padding: 0 10px;
  border: 0;
  border-radius: 8px;
  background: transparent;
  color: var(--oa-text);
  cursor: pointer;
  font: inherit;
}

.top-bar__user:hover {
  background: #f3f6fa;
}
</style>
