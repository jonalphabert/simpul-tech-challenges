<script setup>
import { computed } from 'vue'
import { usePlanPreview } from '../../composables/usePlanPreview'
import { shortages } from '../../utils/eligibility'
import { fmt, km } from '../../utils/format'

const props = defineProps({
  // Valid lines only: [{ productId, quantity }]
  lines: { type: Array, required: true },
  hasDuplicates: { type: Boolean, default: false },
  products: { type: Array, required: true },
  warehouses: { type: Array, required: true },
})

const previewLines = computed(() => (props.hasDuplicates ? [] : props.lines))
const { result, loading, error } = usePlanPreview(previewLines)

const TONES = {
  slate: 'bg-slate-100 text-slate-700',
  orange: 'bg-orange-50 text-orange-900',
  emerald: 'bg-emerald-50 text-emerald-900',
}

const view = computed(() => {
  if (!props.lines.length) return { tone: 'slate', text: 'lengkapi produk dan jumlah untuk melihat hasil plan.' }
  if (props.hasDuplicates) return { tone: 'orange', text: 'ada produk ganda — gabungkan ke satu baris.' }
  if (error.value) return { tone: 'orange', text: `gagal menghitung plan: ${error.value}` }
  if (loading.value || !result.value) return { tone: 'slate', text: 'menghitung plan…' }

  const { min_max_distance: a, min_vans: b } = result.value
  if (result.value.feasible) {
    return {
      tone: 'emerald',
      text: `Terbaik Opsi A: ${km(a.max_distance)} (${a.vans_used} van) · Opsi B: ${b.vans_used} van (${km(b.max_distance)}).`,
    }
  }
  const details = props.lines.map((l) => ({ ...l, product: props.products.find((p) => p.id === l.productId) }))
  const missing = shortages(details, props.warehouses)
    .map((s) => `${s.product.name} kurang ${fmt(s.quantity - s.available)}`)
    .join(', ')
  return {
    tone: 'orange',
    text: `tidak dapat dipenuhi${missing ? ` — ${missing}` : ''}. Order tetap bisa disimpan sebagai infeasible.`,
  }
})
</script>

<template>
  <div :class="['flex flex-wrap gap-1.5 rounded-lg px-3 py-2.5 text-sm', TONES[view.tone]]" role="status">
    <span class="font-semibold">Pratinjau:</span>
    <span>{{ view.text }}</span>
  </div>
</template>
