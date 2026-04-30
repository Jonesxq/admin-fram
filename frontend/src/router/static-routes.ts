import type { RouteRecordRaw } from 'vue-router'

import DashboardView from '@/views/dashboard/DashboardView.vue'
import ForbiddenView from '@/views/errors/ForbiddenView.vue'
import NotFoundView from '@/views/errors/NotFoundView.vue'
import ServerErrorView from '@/views/errors/ServerErrorView.vue'
import LoginView from '@/views/login/LoginView.vue'

export const staticRoutes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView
  },
  {
    path: '/403',
    name: 'Forbidden',
    component: ForbiddenView
  },
  {
    path: '/500',
    name: 'ServerError',
    component: ServerErrorView
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundView
  }
]
