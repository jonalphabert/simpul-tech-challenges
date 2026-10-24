<script setup>
defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' },
})
</script>

<template>
  <div class="flex flex-col items-center gap-3 rounded-xl border border-dashed border-slate-300 bg-white px-6 py-16 text-center">
    <p class="text-base font-medium">{{ title }}</p>
    <p v-if="description" class="max-w-sm text-sm text-slate-600">{{ description }}</p>
    <slot />
  </div>
</template>
