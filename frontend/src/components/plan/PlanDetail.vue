<script setup>
import { computed } from 'vue'
import Chip from '../ui/Chip.vue'
import Icon from '../ui/Icon.vue'
import { stockOf } from '../../utils/eligibility'
import { fmt, km } from '../../utils/format'
import { totalDistance, vansOf } from '../../utils/plans'

const props = defineProps({
  plan: { type: Object, required: true },
  letter: { type: String, required: true },
  warehouses: { type: Array, required: true }, // full warehouses with stock, for "dari stok"
})

const vans = computed(() => vansOf(props.plan))
const headline = computed(
  () => `Terjauh ${km(props.plan.max_distance)} · ${props.plan.vans_used} van · total ${km(totalDistance(props.plan))}`,
)

function stockLabel(warehouseId, productId) {
  const warehouse = props.warehouses.find((w) => w.id === warehouseId)
  return warehouse ? fmt(stockOf(warehouse, productId)) : '–'
}

// The farthest van sets the delivery time, so flag it when there is more than one van.
const isFarthest = (w) => w.distance === props.plan.max_distance && props.plan.vans_used > 1
</script>

<template>
  <div class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-xs">
    <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-200 px-4 py-3">
      <h4 class="text-sm font-semibold">Rincian Plan #{{ plan.rank }} · Opsi {{ letter }}</h4>
      <span class="font-mono text-xs text-slate-500">{{ headline }}</span>
    </div>

    <div class="divide-y divide-slate-100">
      <div v-for="van in vans" :key="van.warehouse.id" class="grid gap-3 px-4 py-4 md:grid-cols-[16rem_minmax(0,1fr)]">
        <div class="flex flex-col gap-1.5">
          <div class="flex items-center gap-2">
            <span class="font-mono text-sm font-semibold">{{ van.warehouse.code }}</span>
            <span class="text-sm text-slate-700">{{ van.warehouse.location }}</span>
          </div>
          <div class="flex flex-wrap items-center gap-1.5">
            <Chip mono :tone="isFarthest(van.warehouse) ? 'orange' : 'slate'" :strong="isFarthest(van.warehouse)">
              {{ km(van.warehouse.distance) }}
            </Chip>
            <Chip :tone="van.warehouse.delivery_fleet === 'refrigerated' ? 'sky' : 'slate'">
              {{ van.warehouse.delivery_fleet === 'refrigerated' ? 'Van berpendingin' : 'Van standar' }}
            </Chip>
          </div>
        </div>

        <ul class="flex flex-col gap-1.5">
          <li
            v-for="line in van.lines"
            :key="line.id_product"
            class="flex items-center justify-between gap-3 rounded-md bg-slate-50 px-3 py-2 text-sm"
          >
            <span class="flex min-w-0 items-center gap-2">
              <Icon v-if="line.product.need_refrigerator" name="snowflake" :size="14" label="Produk dingin" class="shrink-0 text-sky-700" />
              <span class="truncate">{{ line.product.name }}</span>
            </span>
            <span class="shrink-0 font-mono text-slate-800">
              {{ fmt(line.quantity) }} unit
              <span class="text-xs text-slate-500">dari stok {{ stockLabel(van.warehouse.id, line.id_product) }}</span>
            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
