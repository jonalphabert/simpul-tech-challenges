<script setup>
import { computed } from 'vue'

const props = defineProps({
  name: { type: String, required: true },
  size: { type: Number, default: 16 },
  // When set, the icon is announced to screen readers; otherwise it is decorative.
  label: { type: String, default: '' },
})

const ICONS = {
  truck: {
    width: 1.8,
    paths: ['M3 7h11v9H3z', 'M14 10h4l3 3v3h-7', 'M8.5 9.5v4M6.5 11.5h4'],
    circles: [[7, 17.5, 1.8], [17, 17.5, 1.8]],
  },
  plus: { width: 2.2, paths: ['M12 5v14M5 12h14'] },
  close: { width: 2, paths: ['M6 6l12 12M18 6L6 18'] },
  snowflake: { width: 2, paths: ['M12 2v20M4.9 7l14.2 10M4.9 17L19.1 7'] },
  warehouse: { width: 2, paths: ['M3 10l9-6 9 6v10H3z', 'M8 20v-6h8v6'] },
}

const icon = computed(() => ICONS[props.name])
</script>

<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    :stroke-width="icon.width"
    stroke-linecap="round"
    stroke-linejoin="round"
    :role="label ? 'img' : undefined"
    :aria-label="label || undefined"
    :aria-hidden="label ? undefined : 'true'"
  >
    <path v-for="d in icon.paths" :key="d" :d="d" />
    <circle v-for="[cx, cy, r] in icon.circles || []" :key="`${cx}-${cy}`" :cx="cx" :cy="cy" :r="r" />
  </svg>
</template>
