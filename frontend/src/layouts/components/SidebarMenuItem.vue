<script setup lang="ts">
import {
  Document,
  Grid,
  HomeFilled,
  Menu as MenuIcon,
  Setting
} from '@element-plus/icons-vue'

export interface MenuNode {
  id: number | string
  parent_id: number | string | null
  type: string
  title: string
  path: string
  icon: string | null
  sort: number
  children: MenuNode[]
}

defineOptions({
  name: 'SidebarMenuItem'
})

defineProps<{
  item: MenuNode
}>()

const iconMap = {
  Document,
  Grid,
  HomeFilled,
  Menu: MenuIcon,
  Setting
}

function resolveIcon(name: string | null) {
  if (!name) {
    return MenuIcon
  }

  return iconMap[name as keyof typeof iconMap] ?? MenuIcon
}
</script>

<template>
  <ElSubMenu v-if="item.children.length > 0" :index="item.path || String(item.id)">
    <template #title>
      <ElIcon><component :is="resolveIcon(item.icon)" /></ElIcon>
      <span>{{ item.title }}</span>
    </template>

    <SidebarMenuItem v-for="child in item.children" :key="child.id" :item="child" />
  </ElSubMenu>

  <ElMenuItem v-else :index="item.path">
    <ElIcon><component :is="resolveIcon(item.icon)" /></ElIcon>
    <span>{{ item.title }}</span>
  </ElMenuItem>
</template>
