import type { RouteRecordRaw } from 'vue-router'

import AdminLayout from '@/layouts/AdminLayout.vue'
import DashboardView from '@/views/dashboard/DashboardView.vue'
import ForbiddenView from '@/views/errors/ForbiddenView.vue'
import NotFoundView from '@/views/errors/NotFoundView.vue'
import ServerErrorView from '@/views/errors/ServerErrorView.vue'
import DetailView from '@/views/examples/DetailView.vue'
import FormView from '@/views/examples/FormView.vue'
import ListView from '@/views/examples/ListView.vue'
import LoginView from '@/views/login/LoginView.vue'
import ConfigView from '@/views/system/ConfigView.vue'
import DeptView from '@/views/system/DeptView.vue'
import DictView from '@/views/system/DictView.vue'
import LoginLogView from '@/views/system/LoginLogView.vue'
import MenuView from '@/views/system/MenuView.vue'
import OperationLogView from '@/views/system/OperationLogView.vue'
import PostView from '@/views/system/PostView.vue'
import RoleView from '@/views/system/RoleView.vue'
import UserView from '@/views/system/UserView.vue'

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
        path: '/system',
        redirect: '/system/users',
        meta: {
          title: '系统管理'
        }
      },
      {
        path: '/system/users',
        name: 'SystemUsers',
        component: UserView,
        meta: {
          title: '用户管理'
        }
      },
      {
        path: '/system/roles',
        name: 'SystemRoles',
        component: RoleView,
        meta: {
          title: '角色管理'
        }
      },
      {
        path: '/system/menus',
        name: 'SystemMenus',
        component: MenuView,
        meta: {
          title: '菜单管理'
        }
      },
      {
        path: '/system/depts',
        name: 'SystemDepts',
        component: DeptView,
        meta: {
          title: '部门管理'
        }
      },
      {
        path: '/system/posts',
        name: 'SystemPosts',
        component: PostView,
        meta: {
          title: '岗位管理'
        }
      },
      {
        path: '/system/dicts',
        name: 'SystemDicts',
        component: DictView,
        meta: {
          title: '字典管理'
        }
      },
      {
        path: '/system/configs',
        name: 'SystemConfigs',
        component: ConfigView,
        meta: {
          title: '参数配置'
        }
      },
      {
        path: '/system/login-logs',
        name: 'SystemLoginLogs',
        component: LoginLogView,
        meta: {
          title: '登录日志'
        }
      },
      {
        path: '/monitor/login-logs',
        redirect: '/system/login-logs',
        meta: {
          title: '登录日志'
        }
      },
      {
        path: '/system/operation-logs',
        name: 'SystemOperationLogs',
        component: OperationLogView,
        meta: {
          title: '操作日志'
        }
      },
      {
        path: '/monitor/operation-logs',
        redirect: '/system/operation-logs',
        meta: {
          title: '操作日志'
        }
      },
      {
        path: '/examples',
        redirect: '/examples/list',
        meta: {
          title: '示例'
        }
      },
      {
        path: '/examples/list',
        name: 'ExamplesList',
        component: ListView,
        meta: {
          title: '列表示例'
        }
      },
      {
        path: '/examples/form',
        name: 'ExamplesForm',
        component: FormView,
        meta: {
          title: '表单示例'
        }
      },
      {
        path: '/examples/detail',
        name: 'ExamplesDetail',
        component: DetailView,
        meta: {
          title: '详情示例'
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
