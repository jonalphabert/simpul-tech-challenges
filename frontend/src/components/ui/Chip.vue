<script setup>
defineProps({
  tone: { type: String, default: 'slate' }, // slate | sky | orange
  mono: { type: Boolean, default: false },
  strong: { type: Boolean, default: false },
  large: { type: Boolean, default: false },
})

const TONES = {
  slate: 'bg-slate-100 text-slate-700',
  sky: 'bg-sky-100 text-sky-900',
  orange: 'bg-orange-100 text-orange-900',
}
</script>

<template>
  <span
    :class="[
      'inline-flex items-center gap-1 rounded-md text-xs',
      TONES[tone],
      large ? 'px-2 py-1' : 'px-1.5 py-0.5',
      mono && 'font-mono',
      strong ? 'font-semibold' : 'font-medium',
    ]"
  >
    <slot />
  </span>
</template>
