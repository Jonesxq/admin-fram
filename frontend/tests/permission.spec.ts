import { describe, expect, it } from 'vitest'
import { staticRoutes } from '../src/router/static-routes'

describe('static routes', () => {
  it('contains login and dashboard routes', () => {
    expect(staticRoutes.some(route => route.path === '/login')).toBe(true)
    expect(staticRoutes.some(route => route.path === '/dashboard')).toBe(true)
  })
})
