<script setup>
import { computed, ref } from 'vue'
import OrderListItem from './OrderListItem.vue'

const props = defineProps({
  orders: { type: Array, required: true },
  selectedId: { type: Number, default: null },
})

const query = ref('')
const filtered = computed(() => {
  const q = query.value.trim().toLowerCase()
  return q ? props.orders.filter((o) => o.order_number.toLowerCase().includes(q)) : props.orders
})
</script>

<template>
  <aside class="flex flex-col gap-3" aria-label="Daftar order">
    <div class="flex items-center justify-between">
      <h2 class="text-sm font-semibold uppercase tracking-wider text-slate-500">Daftar order</h2>
      <span class="font-mono text-xs text-slate-500">{{ orders.length }} order</span>
    </div>

    <label class="flex flex-col gap-1">
      <span class="sr-only">Cari nomor order</span>
      <input
        v-model="query"
        type="search"
        placeholder="Cari nomor order…"
        class="min-h-[44px] w-full rounded-lg border border-slate-300 bg-white px-3 text-sm placeholder:text-slate-400 focus:border-blue-600 focus:outline-hidden focus:ring-2 focus:ring-blue-600/20"
      />
    </label>

    <div class="flex flex-col gap-2">
      <OrderListItem v-for="o in filtered" :key="o.id" :order="o" :selected="o.id === selectedId" />
      <p
        v-if="!filtered.length"
        class="rounded-lg border border-dashed border-slate-300 px-3 py-6 text-center text-sm text-slate-500"
      >
        <template v-if="query">Tidak ada order yang cocok dengan “{{ query }}”.</template>
        <template v-else>Belum ada order.</template>
      </p>
    </div>
  </aside>
</template>
