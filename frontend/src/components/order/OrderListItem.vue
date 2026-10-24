<script setup>
import { computed } from 'vue'
import StatusBadge from '../ui/StatusBadge.vue'
import { fmt, km } from '../../utils/format'

const props = defineProps({
  order: { type: Object, required: true },
  selected: { type: Boolean, default: false },
})

const units = computed(() => props.order.details.reduce((sum, d) => sum + d.quantity, 0))

const bestLabel = computed(() => {
  const best = props.order.best_plan
  if (!best) return 'belum diplan'
  if (best.status !== 'feasible') return 'stok kurang'
  return `${km(best.max_distance)} · ${best.vans_used} van`
})
</script>

<template>
  <RouterLink
    :to="`/orders/${order.id}`"
    :aria-current="selected ? 'true' : undefined"
    :class="[
      'flex min-h-[44px] w-full flex-col gap-1.5 rounded-lg border bg-white px-3 py-2.5 text-left text-slate-900',
      selected ? 'border-blue-600 shadow-xs ring-2 ring-blue-600/20' : 'border-slate-200 hover:border-slate-400',
    ]"
  >
    <div class="flex items-center justify-between gap-2">
      <span class="font-mono text-sm font-semibold">{{ order.order_number }}</span>
      <StatusBadge :status="order.best_plan?.status ?? null" />
    </div>
    <div class="flex items-center justify-between gap-2 text-xs text-slate-600">
      <span>{{ order.details.length }} produk · {{ fmt(units) }} unit</span>
      <span class="font-mono">{{ bestLabel }}</span>
    </div>
  </RouterLink>
</template>
