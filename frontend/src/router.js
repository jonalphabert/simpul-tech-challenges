import { createRouter, createWebHistory } from 'vue-router'
import OrdersLayout from './views/OrdersLayout.vue'
import OrderEmptyView from './views/OrderEmptyView.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/orders' },
    {
      path: '/orders',
      component: OrdersLayout,
      children: [
        { path: '', component: OrderEmptyView },
      ],
    },
  ],
})
