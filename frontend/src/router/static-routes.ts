import type { RouteRecordRaw } from 'vue-router'

import AdminLayout from '@/layouts/AdminLayout.vue'
import DashboardView from '@/views/dashboard/DashboardView.vue'
import ForbiddenView from '@/views/errors/ForbiddenView.vue'
import NotFoundView from '@/views/errors/NotFoundView.vue'
import ServerErrorView from '@/views/errors/ServerErrorView.vue'
import LoginView from '@/views/login/LoginView.vue'

export const staticRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    component: AdminLayout,
    redirect: '/dashboard',
    children: [
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: DashboardView,
        meta: {
          title: '仪表盘',
          affix: true
        }
      },
      {
        path: '/system/:pathMatch(.*)*',
        name: 'SystemPlaceholder',
        component: NotFoundView,
        meta: {
          title: '系统管理'
        }
      },
      {
        path: '/examples/:pathMatch(.*)*',
        name: 'ExamplesPlaceholder',
        component: NotFoundView,
        meta: {
          title: '示例'
        }
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: {
      hiddenTab: true
    }
  },
  {
    path: '/403',
    name: 'Forbidden',
    component: ForbiddenView,
    meta: {
      hiddenTab: true
    }
  },
  {
    path: '/500',
    name: 'ServerError',
    component: ServerErrorView,
    meta: {
      hiddenTab: true
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundView,
    meta: {
      hiddenTab: true
    }
  }
]
