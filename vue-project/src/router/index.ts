import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/查询',
      name: '查询',
      component: () => import('../views/查询.vue')
    },
    {
      path: '/策略',
      name: '策略',
      component: () => import('../views/策略.vue')
    },
    {
      path: '/交易',
      name: '交易',
      component: () => import('../views/交易.vue')
    },
    {
      path: '/设置',
      name: '设置',
      component: () => import('../views/设置.vue')
    }
  ]
})

export default router
