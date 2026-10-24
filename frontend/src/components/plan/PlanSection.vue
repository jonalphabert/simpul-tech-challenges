<script setup>
import { computed } from 'vue'
import SegmentedControl from '../ui/SegmentedControl.vue'
import PlanDetail from './PlanDetail.vue'
import PlanSummaryCard from './PlanSummaryCard.vue'
import { OBJECTIVES, plansFor, warehouseKey } from '../../utils/plans'

const props = defineProps({
  plans: { type: Array, required: true }, // all saved plans of the order (both objectives)
  letter: { type: String, required: true }, // 'A' | 'B'
  rank: { type: Number, required: true },
  warehouses: { type: Array, required: true },
})
const emit = defineEmits(['update:letter', 'update:rank'])

const objectiveItems = Object.entries(OBJECTIVES).map(([letter, o]) => ({ value: letter, prefix: letter, label: o.label }))

const visible = computed(() => plansFor(props.plans, props.letter))
const selected = computed(() => visible.value.find((p) => p.rank === props.rank) ?? visible.value[0])

const compareNote = computed(() => {
  const [a] = plansFor(props.plans, 'A')
  const [b] = plansFor(props.plans, 'B')
  if (!a || !b) return ''
  return warehouseKey(a) === warehouseKey(b)
    ? 'Opsi A dan B merekomendasikan kombinasi yang sama.'
    : 'Opsi A dan B memberi rekomendasi berbeda.'
})
</script>

<template>
  <div class="flex flex-col gap-4">
    <div class="flex flex-wrap items-end justify-between gap-3">
      <div class="flex flex-col gap-1">
        <h3 class="text-lg font-semibold">Plan pengiriman</h3>
        <p class="text-sm text-slate-600">
          Menampilkan {{ visible.length }} plan teratas · kombinasi gudang minimal (tanpa van yang tidak perlu).
        </p>
      </div>
      <SegmentedControl
        :items="objectiveItems"
        :active="letter"
        tone="dark"
        aria-label="Tujuan optimasi"
        @select="emit('update:letter', $event)"
      />
    </div>

    <p class="text-sm text-slate-600">
      {{ OBJECTIVES[letter].hint }} <span class="font-medium text-slate-800">{{ compareNote }}</span>
    </p>

    <div class="grid grid-cols-[repeat(auto-fill,minmax(min(11rem,100%),1fr))] gap-3">
      <PlanSummaryCard
        v-for="plan in visible"
        :key="plan.id"
        :plan="plan"
        :selected="plan.id === selected?.id"
        @select="emit('update:rank', plan.rank)"
      />
    </div>

    <PlanDetail v-if="selected" :plan="selected" :letter="letter" :warehouses="warehouses" />
  </div>
</template>
