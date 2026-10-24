<script setup>
import { computed } from 'vue'
import { km } from '../../utils/format'
import { vansOf } from '../../utils/plans'

const props = defineProps({
  plan: { type: Object, required: true },
  selected: { type: Boolean, default: false },
})
defineEmits(['select'])

const codes = computed(() => vansOf(props.plan).map((v) => v.warehouse.code).join(' · '))
</script>

<template>
  <button
    type="button"
    :aria-pressed="selected ? 'true' : 'false'"
    :class="[
      'flex min-h-[44px] flex-col gap-2 rounded-xl border-2 bg-white p-3 text-left shadow-xs',
      selected ? 'border-blue-700' : 'border-transparent ring-1 ring-slate-200 hover:ring-slate-400',
    ]"
    @click="$emit('select')"
  >
    <div class="flex items-center justify-between">
      <span class="text-xs font-semibold uppercase tracking-wider text-slate-500">Plan #{{ plan.rank }}</span>
      <span
        v-if="plan.rank === 1"
        class="rounded-sm bg-blue-700 px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-white"
      >
        Terbaik
      </span>
    </div>
    <div class="flex items-baseline gap-3">
      <div class="flex flex-col">
        <span class="font-mono text-xl font-semibold">{{ km(plan.max_distance) }}</span>
        <span class="text-[11px] text-slate-500">terjauh</span>
      </div>
      <div class="flex flex-col">
        <span class="font-mono text-xl font-semibold">{{ plan.vans_used }}</span>
        <span class="text-[11px] text-slate-500">van</span>
      </div>
    </div>
    <span class="truncate font-mono text-xs text-slate-600">{{ codes }}</span>
  </button>
</template>
