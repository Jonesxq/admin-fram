<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import type { AuthMenu } from '@/api/auth'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'

import SidebarMenuItem, { type MenuNode } from './SidebarMenuItem.vue'

const fallbackMenus: MenuNode[] = [
  {
    id: 'dashboard',
    parent_id: null,
    type: 'menu',
    title: '仪表盘',
    path: '/dashboard',
    icon: 'HomeFilled',
    sort: 0,
    children: []
  }
]

const authStore = useAuthStore()
const appStore = useAppStore()
const route = useRoute()

function normalizeMenu(menu: AuthMenu): MenuNode {
  return {
    id: menu.id,
    parent_id: menu.parent_id,
    type: menu.type,
    title: menu.title,
    path: menu.path,
    icon: menu.icon,
    sort: menu.sort,
    children: []
  }
}

function isNavigable(menu: Pick<MenuNode, 'type' | 'path'>) {
  return menu.type !== 'button' && Boolean(menu.path)
}

function buildTree(menus: AuthMenu[]) {
  const nodes = menus.filter(isNavigable).map(normalizeMenu)
  const nodeMap = new Map<MenuNode['id'], MenuNode>()
  const roots: MenuNode[] = []

  nodes.forEach(node => nodeMap.set(node.id, node))
  nodes.forEach(node => {
    if (node.parent_id !== null && nodeMap.has(node.parent_id)) {
      nodeMap.get(node.parent_id)?.children.push(node)
    } else {
      roots.push(node)
    }
  })

  const sortTree = (items: MenuNode[]) => {
    items.sort((first, second) => first.sort - second.sort)
    items.forEach(item => sortTree(item.children))
    return items
  }

  return sortTree(roots)
}

const menus = computed(() => {
  const tree = buildTree(authStore.menus)

  return tree.length > 0 ? tree : fallbackMenus
})

</script>

<template>
  <div class="sidebar-menu">
    <RouterLink class="sidebar-menu__brand" to="/dashboard">
      <span class="sidebar-menu__mark">OA</span>
      <strong v-show="!appStore.sidebarCollapsed">Open Admin</strong>
    </RouterLink>

    <ElMenu
      :collapse="appStore.sidebarCollapsed"
      :default-active="route.path"
      router
      unique-opened
    >
      <SidebarMenuItem v-for="item in menus" :key="item.id" :item="item" />
    </ElMenu>
  </div>
</template>

<style scoped>
.sidebar-menu {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}

.sidebar-menu__brand {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 64px;
  padding: 0 16px;
  border-bottom: 1px solid var(--oa-border);
  color: var(--oa-text);
  text-decoration: none;
  white-space: nowrap;
}

.sidebar-menu__mark {
  display: inline-flex;
  width: 32px;
  height: 32px;
  flex: 0 0 32px;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: var(--oa-primary);
  color: #ffffff;
  font-size: 13px;
  font-weight: 800;
}
</style>
