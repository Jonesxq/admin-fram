import { defineStore } from 'pinia'

interface AppState {
  sidebarCollapsed: boolean
  themePanelOpen: boolean
}

export const useAppStore = defineStore('app', {
  state: (): AppState => ({
    sidebarCollapsed: false,
    themePanelOpen: false
  }),
  actions: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    },
    setSidebarCollapsed(collapsed: boolean) {
      this.sidebarCollapsed = collapsed
    },
    toggleThemePanel() {
      this.themePanelOpen = !this.themePanelOpen
    },
    closeThemePanel() {
      this.themePanelOpen = false
    }
  }
})
