import { createRouter, createWebHistory } from 'vue-router';
import index from '@/views/index.vue';
import login from '@/views/login.vue';
import register from '@/views/Register.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/login', // 将默认路径重定向到login
    },
    {
      path: '/index',
      name: 'index',
      component: index,
      children: [
        {
          path: '查询',
          name: '查询',
          component: () => import('../views/查询.vue'),
        },
        {
          path: 'stock/:code',
          name: 'StockDetail',
          component: () => import('../views/StockDetail.vue'),
        },
        {
          path: '策略',
          name: '策略',
          component: () => import('../views/策略.vue'),
        },
        {
          path: '策略代码/:name',
          name: '策略代码',
          component: () => import('../views/策略代码.vue'),
        },
        {
          path: '交易',
          name: '交易',
          component: () => import('../views/交易.vue'),
        },
        {
          path: '设置',
          name: '设置',
          component: () => import('../views/设置.vue'),
        },
      ],
    },
    {
      path: '/login',
      name: 'login',
      component: login,
    },
    {
      path: '/register',
      name: 'register',
      component: register,
    },
  ],
});

export default router;
