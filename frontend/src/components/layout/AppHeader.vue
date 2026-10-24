<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Icon from '../ui/Icon.vue'
import SegmentedControl from '../ui/SegmentedControl.vue'

const props = defineProps({
  orderCount: { type: Number, default: 0 },
  warehouseCount: { type: Number, default: 0 },
})

const route = useRoute()
const router = useRouter()

const activeTab = computed(() => (route.path.startsWith('/warehouses') ? 'warehouses' : 'orders'))
const tabs = computed(() => [
  { value: 'orders', label: 'Order', count: props.orderCount, to: '/orders' },
  { value: 'warehouses', label: 'Warehouse', count: props.warehouseCount, to: '/warehouses' },
])
</script>

<template>
  <header class="border-b border-slate-200 bg-white">
    <div class="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-4 py-3 sm:px-6">
      <div class="flex items-center gap-3">
        <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-900 text-white">
          <Icon name="truck" :size="22" />
        </div>
        <div class="flex flex-col">
          <span class="text-[11px] font-semibold uppercase tracking-[0.14em] text-slate-500">Distribusi Medis</span>
          <span class="text-lg font-semibold leading-tight">Delivery Planner</span>
        </div>
      </div>

      <nav aria-label="Navigasi utama">
        <SegmentedControl :items="tabs" :active="activeTab" />
      </nav>

      <button
        type="button"
        class="inline-flex min-h-[44px] items-center gap-2 rounded-lg bg-blue-700 px-4 text-sm font-semibold text-white shadow-xs hover:bg-blue-800 focus:outline-hidden focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
        @click="router.push('/orders/new')"
      >
        <Icon name="plus" />
        Order baru
      </button>
    </div>
  </header>
</template>
