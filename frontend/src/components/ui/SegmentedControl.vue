<script setup>
// Pill group used for the main navigation (items with `to`) and the objective toggle.
defineProps({
  items: { type: Array, required: true }, // { value, label, prefix?, count?, to? }
  active: { type: String, default: '' },
  tone: { type: String, default: 'light' }, // light: bg-slate-100, dark: bg-slate-200/70
  ariaLabel: { type: String, default: '' },
})
defineEmits(['select'])

const ON = 'inline-flex min-h-[40px] items-center gap-1.5 rounded-md bg-white px-3 text-sm font-semibold text-slate-900 shadow-xs'
const OFF = 'inline-flex min-h-[40px] items-center gap-1.5 rounded-md px-3 text-sm font-medium text-slate-600 hover:text-slate-900'
</script>

<template>
  <div
    :class="['flex flex-wrap gap-1 rounded-lg p-1', tone === 'dark' ? 'bg-slate-200/70' : 'bg-slate-100']"
    :role="items[0]?.to ? undefined : 'group'"
    :aria-label="ariaLabel || undefined"
  >
    <template v-for="item in items" :key="item.value">
      <RouterLink
        v-if="item.to"
        :to="item.to"
        :class="item.value === active ? ON : OFF"
        :aria-current="item.value === active ? 'page' : undefined"
      >
        {{ item.label }}
        <span v-if="item.count !== undefined" class="font-mono text-xs text-slate-500">{{ item.count }}</span>
      </RouterLink>
      <button
        v-else
        type="button"
        :class="item.value === active ? ON : OFF"
        :aria-pressed="item.value === active ? 'true' : 'false'"
        @click="$emit('select', item.value)"
      >
        <span v-if="item.prefix" class="font-mono text-xs">{{ item.prefix }}</span>
        {{ item.label }}
      </button>
    </template>
  </div>
</template>
