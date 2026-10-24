<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import OrderList from '../components/order/OrderList.vue'
import ErrorAlert from '../components/ui/ErrorAlert.vue'
import { useOrders } from '../stores/orders'

const route = useRoute()
const { orders, error } = useOrders()

const selectedId = computed(() => (route.params.id ? Number(route.params.id) : null))
</script>

<template>
  <main class="mx-auto grid max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[20rem_minmax(0,1fr)]">
    <div class="flex flex-col gap-3">
      <ErrorAlert :message="error" />
      <OrderList :orders="orders" :selected-id="selectedId" />
    </div>
    <section class="flex min-w-0 flex-col gap-6">
      <RouterView />
    </section>
  </main>
</template>
