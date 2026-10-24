<script setup>
import { onMounted } from 'vue'
import AppHeader from './components/layout/AppHeader.vue'
import { useCatalog } from './stores/catalog'
import { useOrders } from './stores/orders'

const { warehouses, load: loadCatalog } = useCatalog()
const { orders, refresh: refreshOrders } = useOrders()

onMounted(() => {
  loadCatalog()
  refreshOrders()
})
</script>

<template>
  <div class="min-h-screen bg-slate-50 font-sans text-slate-900 antialiased">
    <AppHeader :order-count="orders.length" :warehouse-count="warehouses.length" />
    <RouterView />
  </div>
</template>
