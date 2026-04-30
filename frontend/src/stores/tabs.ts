import { defineStore } from 'pinia'
import type { RouteLocationNormalizedLoaded } from 'vue-router'

export interface VisitedTab {
  path: string
  fullPath: string
  title: string
  affix: boolean
}

interface TabsState {
  visitedTabs: VisitedTab[]
}

function resolveTitle(route: RouteLocationNormalizedLoaded) {
  return String(route.meta.title ?? route.name ?? route.path)
}

export const useTabsStore = defineStore('tabs', {
  state: (): TabsState => ({
    visitedTabs: []
  }),
  actions: {
    addTab(route: RouteLocationNormalizedLoaded) {
      if (!route.name || route.meta.hiddenTab) {
        return
      }

      const existing = this.visitedTabs.find(tab => tab.path === route.path)

      if (existing) {
        existing.fullPath = route.fullPath
        existing.title = resolveTitle(route)
        return
      }

      this.visitedTabs.push({
        path: route.path,
        fullPath: route.fullPath,
        title: resolveTitle(route),
        affix: Boolean(route.meta.affix)
      })
    },
    removeTab(path: string) {
      const tab = this.visitedTabs.find(item => item.path === path)

      if (tab?.affix) {
        return this.visitedTabs
      }

      this.visitedTabs = this.visitedTabs.filter(item => item.path !== path)

      return this.visitedTabs
    },
    removeOthers(path: string) {
      this.visitedTabs = this.visitedTabs.filter(tab => tab.affix || tab.path === path)

      return this.visitedTabs
    },
    clearTabs() {
      this.visitedTabs = this.visitedTabs.filter(tab => tab.affix)
    },
    resetTabs() {
      this.visitedTabs = []
    }
  }
})
