import { createRouter, createWebHistory } from 'vue-router'
import OrdersLayout from './views/OrdersLayout.vue'
import OrderEmptyView from './views/OrderEmptyView.vue'
import OrderCreateView from './views/OrderCreateView.vue'
import OrderDetailView from './views/OrderDetailView.vue'
import WarehousesView from './views/WarehousesView.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/orders' },
    {
      path: '/orders',
      component: OrdersLayout,
      children: [
        { path: '', component: OrderEmptyView },
        { path: 'new', component: OrderCreateView },
        { path: ':id(\\d+)', component: OrderDetailView, props: true },
      ],
    },
    // ?order=&objective=&rank= highlights one plan on the warehouse page.
    { path: '/warehouses', component: WarehousesView },
  ],
})
