<script setup>
import { computed } from 'vue'
import Chip from '../ui/Chip.vue'
import { canShipCold } from '../../utils/eligibility'
import { fmt, km } from '../../utils/format'

const props = defineProps({
  warehouse: { type: Object, required: true },
  // null: no plan highlighted; otherwise units this warehouse ships (0 = not used).
  shippedUnits: { type: Number, default: null },
})

const highlighting = computed(() => props.shippedUnits !== null)
const used = computed(() => props.shippedUnits > 0)
const refrigeratedFleet = computed(() => props.warehouse.delivery_fleet === 'refrigerated')
</script>

<template>
  <article
    :class="[
      'flex flex-col gap-3 rounded-xl border-2 bg-white p-4',
      used
        ? 'border-blue-700 shadow-xs'
        : highlighting
          ? 'border-transparent opacity-60 ring-1 ring-slate-200'
          : 'border-transparent shadow-xs ring-1 ring-slate-200',
    ]"
  >
    <div class="flex items-start justify-between gap-2">
      <div class="flex flex-col">
        <span class="font-mono text-sm font-semibold">{{ warehouse.code }}</span>
        <span class="text-base font-medium">{{ warehouse.location }}</span>
      </div>
      <span class="font-mono text-lg font-semibold">{{ km(warehouse.distance) }}</span>
    </div>

    <dl class="grid grid-cols-[auto_minmax(0,1fr)] gap-x-3 gap-y-1 text-sm">
      <dt class="text-slate-500">Cold storage</dt>
      <dd :class="warehouse.refrigerated_storage_available ? 'font-medium text-slate-900' : 'text-slate-500'">
        {{ warehouse.refrigerated_storage_available ? 'Ada' : 'Tidak ada' }}
      </dd>
      <dt class="text-slate-500">Armada</dt>
      <dd :class="refrigeratedFleet ? 'font-medium text-slate-900' : 'text-slate-500'">
        {{ refrigeratedFleet ? 'Van berpendingin' : 'Van standar' }}
      </dd>
    </dl>

    <Chip large :tone="canShipCold(warehouse) ? 'sky' : 'slate'" class="self-start">
      {{ canShipCold(warehouse) ? 'Bisa kirim produk dingin' : 'Hanya produk suhu ruang' }}
    </Chip>

    <span v-if="used" class="rounded-md bg-blue-700 px-2 py-1 text-xs font-semibold text-white">
      Dipakai di plan · {{ fmt(shippedUnits) }} unit
    </span>
  </article>
</template>
