<script setup>
import { computed } from 'vue'
import Chip from '../ui/Chip.vue'
import { eligibleStock } from '../../utils/eligibility'
import { fmt } from '../../utils/format'

const props = defineProps({
  details: { type: Array, required: true }, // order.details with product
  warehouses: { type: Array, required: true },
})

const rows = computed(() =>
  props.details.map((d) => {
    const eligible = eligibleStock(props.warehouses, d.product)
    return {
      ...d,
      available: eligible.total,
      ok: eligible.total >= d.quantity,
      codes: eligible.warehouses.length ? eligible.warehouses.map((w) => w.code).join(', ') : 'tidak ada gudang',
    }
  }),
)
</script>

<template>
  <div class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-xs">
    <div class="border-b border-slate-200 px-4 py-3">
      <h3 class="text-sm font-semibold">Isi order</h3>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full min-w-[560px] text-sm">
        <thead class="bg-slate-50 text-left text-xs uppercase tracking-wider text-slate-500">
          <tr>
            <th scope="col" class="px-4 py-2 font-medium">Produk</th>
            <th scope="col" class="px-4 py-2 font-medium">Penyimpanan</th>
            <th scope="col" class="px-4 py-2 text-right font-medium">Dipesan</th>
            <th scope="col" class="px-4 py-2 text-right font-medium">Stok memenuhi syarat</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="row in rows" :key="row.id_product">
            <td class="px-4 py-2.5">
              <div class="font-medium">{{ row.product.name }}</div>
              <div class="text-xs text-slate-500">{{ row.product.category }}</div>
            </td>
            <td class="px-4 py-2.5">
              <Chip :tone="row.product.need_refrigerator ? 'sky' : 'slate'">
                {{ row.product.need_refrigerator ? 'Rantai dingin' : 'Suhu ruang' }}
              </Chip>
            </td>
            <td class="px-4 py-2.5 text-right font-mono">{{ fmt(row.quantity) }} unit</td>
            <td class="px-4 py-2.5 text-right">
              <span :class="row.ok ? 'font-mono text-slate-800' : 'font-mono font-semibold text-orange-800'">
                {{ fmt(row.available) }} unit
              </span>
              <div class="text-xs text-slate-500">{{ row.codes }}</div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
