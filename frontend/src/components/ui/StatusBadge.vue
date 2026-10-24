<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: { type: String, default: null }, // 'feasible' | 'infeasible' | null (not planned)
})

const STYLES = {
  feasible: { label: 'Feasible', cls: 'bg-emerald-100 text-emerald-900' },
  infeasible: { label: 'Infeasible', cls: 'bg-orange-100 text-orange-900' },
  none: { label: 'Belum diplan', cls: 'bg-slate-100 text-slate-700' },
}

const style = computed(() => STYLES[props.status] ?? STYLES.none)
</script>

<template>
  <span :class="['rounded-full px-2 py-0.5 text-xs font-semibold', style.cls]">{{ style.label }}</span>
</template>
