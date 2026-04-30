import { mount } from '@vue/test-utils'
import ElementPlus from 'element-plus'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import { beforeEach, describe, expect, it } from 'vitest'

import SidebarMenu from '../src/layouts/components/SidebarMenu.vue'
import { useAuthStore } from '../src/stores/auth'

describe('SidebarMenu', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders nested menu grandchildren from auth menus', async () => {
    const authStore = useAuthStore()
    const router = createRouter({
      history: createWebHistory(),
      routes: [
        {
          path: '/',
          component: { template: '<div />' }
        },
        {
          path: '/dashboard',
          component: { template: '<div />' }
        },
        {
          path: '/system/users/list',
          component: { template: '<div />' }
        }
      ]
    })

    authStore.menus = [
      {
        id: 1,
        parent_id: null,
        type: 'menu',
        title: '系统管理',
        path: '/system',
        component: null,
        permission: null,
        icon: 'Setting',
        sort: 1
      },
      {
        id: 2,
        parent_id: 1,
        type: 'menu',
        title: '用户中心',
        path: '/system/users',
        component: null,
        permission: null,
        icon: null,
        sort: 1
      },
      {
        id: 3,
        parent_id: 2,
        type: 'menu',
        title: '用户列表',
        path: '/system/users/list',
        component: null,
        permission: null,
        icon: null,
        sort: 1
      }
    ]

    router.push('/')
    await router.isReady()

    const wrapper = mount(SidebarMenu, {
      global: {
        plugins: [router, ElementPlus]
      }
    })

    expect(wrapper.text()).toContain('系统管理')
    expect(wrapper.text()).toContain('用户中心')
    expect(wrapper.text()).toContain('用户列表')
  })
})
