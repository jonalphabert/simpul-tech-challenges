<script setup>
import { computed } from 'vue'
import Icon from '../ui/Icon.vue'
import { isBlocked, stockOf } from '../../utils/eligibility'
import { fmt, km } from '../../utils/format'

const props = defineProps({
  products: { type: Array, required: true },
  warehouses: { type: Array, required: true },
  // null, or { usedIds: Set<warehouseId>, productIds: Set<productId>, ship(wId, pId) => qty }
  highlight: { type: Object, default: null },
})

const isUsed = (w) => !!props.highlight?.usedIds.has(w.id)

const rows = computed(() =>
  props.products.map((p) => {
    let total = 0
    const cells = props.warehouses.map((w) => {
      const stock = stockOf(w, p.id)
      const blocked = isBlocked(w, p)
      if (!blocked) total += stock
      const cls = ['px-3 py-2.5 text-right align-top font-mono']
      if (blocked) cls.push('bg-slate-100 text-slate-500 line-through decoration-slate-400')
      else cls.push(stock === 0 ? 'text-slate-400' : 'text-slate-800')
      if (isUsed(w)) cls.push('bg-blue-50')
      return { id: w.id, text: stock ? fmt(stock) : '—', ship: props.highlight?.ship(w.id, p.id) ?? 0, cls }
    })
    const dimmed = props.highlight && !props.highlight.productIds.has(p.id)
    return { product: p, cells, total, dimmed }
  }),
)
</script>

<template>
  <div class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-xs">
    <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 px-4 py-3">
      <h3 class="text-sm font-semibold">Stok per warehouse</h3>
      <div class="flex flex-wrap items-center gap-4 text-xs text-slate-600">
        <span class="flex items-center gap-1.5"><span class="inline-block h-3 w-3 rounded-xs bg-slate-200"></span>Tidak bisa kirim produk dingin</span>
        <span class="flex items-center gap-1.5"><span class="inline-block h-3 w-3 rounded-xs bg-blue-700"></span>Dikirim di plan</span>
      </div>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full min-w-[860px] text-sm">
        <thead class="bg-slate-50 text-xs uppercase tracking-wider text-slate-500">
          <tr>
            <th scope="col" class="px-4 py-2 text-left font-medium">Produk</th>
            <th
              v-for="w in warehouses"
              :key="w.id"
              scope="col"
              :class="isUsed(w) ? 'bg-blue-100 px-3 py-2 text-right font-semibold text-blue-950' : 'px-3 py-2 text-right font-medium'"
            >
              <div class="font-mono normal-case">{{ w.code }}</div>
              <div class="font-normal normal-case tracking-normal">{{ km(w.distance) }}</div>
            </th>
            <th scope="col" class="px-4 py-2 text-right font-medium">Total</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="row in rows" :key="row.product.id" :class="['bg-white', row.dimmed && 'opacity-50']">
            <th scope="row" class="px-4 py-2.5 text-left font-normal">
              <div class="flex items-center gap-2">
                <Icon v-if="row.product.need_refrigerator" name="snowflake" :size="14" label="Produk dingin" class="shrink-0 text-sky-700" />
                <span class="font-medium">{{ row.product.name }}</span>
              </div>
              <div class="text-xs text-slate-500">
                {{ row.product.category }}{{ row.product.need_refrigerator ? ' · rantai dingin' : '' }}
              </div>
            </th>
            <td v-for="cell in row.cells" :key="cell.id" :class="cell.cls">
              <div>{{ cell.text }}</div>
              <div v-if="cell.ship > 0" class="mt-0.5 inline-block rounded-sm bg-blue-700 px-1.5 text-xs font-semibold text-white">
                kirim {{ fmt(cell.ship) }}
              </div>
            </td>
            <td class="px-4 py-2.5 text-right font-mono text-slate-700">{{ fmt(row.total) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
