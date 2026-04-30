import { createRouter, createWebHistory } from 'vue-router'

import { staticRoutes } from './static-routes'

export const router = createRouter({
  history: createWebHistory(),
  routes: staticRoutes
})
