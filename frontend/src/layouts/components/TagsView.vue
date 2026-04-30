<script setup lang="ts">
import { Close } from '@element-plus/icons-vue'
import { storeToRefs } from 'pinia'
import { watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useTabsStore, type VisitedTab } from '@/stores/tabs'

const route = useRoute()
const router = useRouter()
const tabsStore = useTabsStore()
const { visitedTabs } = storeToRefs(tabsStore)

watch(
  () => route.fullPath,
  () => tabsStore.addTab(route),
  { immediate: true }
)

async function closeTab(tab: VisitedTab) {
  if (tab.affix) {
    return
  }

  tabsStore.removeTab(tab.path)

  if (tab.path !== route.path) {
    return
  }

  const nextTab = visitedTabs.value[visitedTabs.value.length - 1]

  await router.push(nextTab?.fullPath ?? '/dashboard')
}
</script>

<template>
  <nav class="tags-view" aria-label="访问标签">
    <RouterLink
      v-for="tab in visitedTabs"
      :key="tab.path"
      class="tags-view__item"
      :class="{ 'is-active': tab.path === route.path }"
      :to="tab.fullPath"
    >
      <span>{{ tab.title }}</span>
      <ElButton
        v-if="!tab.affix"
        circle
        text
        size="small"
        :icon="Close"
        aria-label="关闭标签"
        @click.prevent="closeTab(tab)"
      />
    </RouterLink>
  </nav>
</template>

<style scoped>
.tags-view {
  display: flex;
  min-height: 40px;
  align-items: center;
  gap: 8px;
  overflow-x: auto;
  border-bottom: 1px solid var(--oa-border);
  background: var(--oa-panel);
  padding: 6px 16px;
}

.tags-view__item {
  display: inline-flex;
  height: 28px;
  align-items: center;
  gap: 4px;
  flex: 0 0 auto;
  border: 1px solid var(--oa-border);
  border-radius: 8px;
  background: #ffffff;
  color: var(--oa-muted);
  font-size: 13px;
  padding: 0 6px 0 10px;
  text-decoration: none;
}

.tags-view__item.is-active {
  border-color: rgba(15, 118, 110, 0.28);
  background: #f0fdfa;
  color: var(--oa-primary);
  font-weight: 700;
}
</style>
