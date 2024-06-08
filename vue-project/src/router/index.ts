     //配置子路由界面的路径
import { createRouter, createWebHistory } from 'vue-router'
import index from "@/views/index.vue"
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'index',
      component: index,
      children: [
      {
        path: '查询',
        name: '查询',
        component: () => import('../views/查询.vue'),
        },
      {
        path: 'stock/:code',  // 将此路由移出'查询'的子路由，使其成为顶级路由
        name: 'StockDetail',
        component: () => import('../views/StockDetail.vue')
      },
      {
        path: '策略',
        name: '策略',
        component: () => import('../views/策略.vue')
      },
      {
        path: '交易',
        name: '交易',
        component: () => import('../views/交易.vue')
        },
        {
          path: '持仓',
          name: '持仓',
          component: () => import('../views/持仓.vue')
        },
      {
        path: '设置',
        name: '设置',
        component: () => import('../views/设置.vue')
      } 
      ]
    },
  ]
})

export default router
