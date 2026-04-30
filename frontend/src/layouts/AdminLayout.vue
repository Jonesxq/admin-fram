<script setup lang="ts">
import { storeToRefs } from 'pinia'

import { useAppStore } from '@/stores/app'

import SidebarMenu from './components/SidebarMenu.vue'
import TagsView from './components/TagsView.vue'
import TopBar from './components/TopBar.vue'

const appStore = useAppStore()
const { sidebarCollapsed } = storeToRefs(appStore)
</script>

<template>
  <section class="oa-shell" :class="{ 'is-collapsed': sidebarCollapsed }">
    <aside class="oa-sidebar">
      <SidebarMenu />
    </aside>

    <section class="oa-main">
      <TopBar />
      <TagsView />
      <main class="oa-content">
        <section class="oa-view">
          <RouterView />
        </section>
      </main>
    </section>
  </section>
</template>
